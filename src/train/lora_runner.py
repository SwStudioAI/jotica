import argparse
import os
import time
import tarfile
import torch
import json
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, DataCollatorForLanguageModeling, Trainer, TrainingArguments
from peft import LoraConfig, get_peft_model
from ..config import cfg
from ..utils.io_utils import write_text
from ..utils.supa import upload_ckpt

def zip_dir(src, out_tar_gz):
    with tarfile.open(out_tar_gz, "w:gz") as tar:
        tar.add(src, arcname=os.path.basename(src))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--base_model", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--output_dir", required=True)
    ap.add_argument("--run_name", required=True)
    ap.add_argument("--epochs", type=int, default=2)
    ap.add_argument("--batch_size", type=int, default=2)
    ap.add_argument("--lr", type=float, default=2e-4)
    ap.add_argument("--save_steps", type=int, default=200)
    ap.add_argument("--save_total", type=int, default=3)
    ap.add_argument("--max_seq_len", type=int, default=1024)
    args = ap.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    tok = AutoTokenizer.from_pretrained(args.base_model, use_fast=True)
    if tok.pad_token is None: 
        tok.pad_token = tok.eos_token

    ds = load_dataset("json", data_files={"train": args.data})["train"]

    from .formatters import format_row
    ds = ds.map(lambda r: {"text": format_row(r)}, remove_columns=ds.column_names)
    ds = ds.map(lambda b: tok(b["text"], truncation=True, max_length=args.max_seq_len), batched=True, remove_columns=["text"])
    collator = DataCollatorForLanguageModeling(tok, mlm=False)

    base = AutoModelForCausalLM.from_pretrained(args.base_model, torch_dtype="auto", device_map="auto")
    lcfg = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05, task_type="CAUSAL_LM", bias="none",
                      target_modules=["q_proj","v_proj"])
    model = get_peft_model(base, lcfg)

    targs = TrainingArguments(
        output_dir=args.output_dir,
        run_name=args.run_name,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=4,
        num_train_epochs=args.epochs,
        learning_rate=args.lr,
        fp16=True,
        logging_steps=25,
        save_strategy="steps",
        save_steps=args.save_steps,
        save_total_limit=args.save_total,
        evaluation_strategy="no",
        report_to="none"
    )

    trainer = Trainer(model=model, args=targs, train_dataset=ds, data_collator=collator)
    
    # Training with automatic checkpoint backup
    print(f"🚀 Starting LoRA training: {args.run_name}")
    print(f"   Model: {args.base_model}")
    print(f"   Dataset: {len(ds)} samples")
    print(f"   Epochs: {args.epochs}")
    print(f"   Batch size: {args.batch_size}")
    print(f"   Output: {args.output_dir}")
    
    try:
        # Start training
        trainer.train()
        print("✅ Training completed successfully!")
        
    except KeyboardInterrupt:
        print("⚠️ Training interrupted by user")
        
    except Exception as e:
        print(f"❌ Training failed: {str(e)}")
        
    finally:
        print("\n📦 Saving final checkpoint...")
        
        # Save model and tokenizer
        trainer.save_model(args.output_dir)
        tok.save_pretrained(args.output_dir)
        print(f"✅ Model saved to: {args.output_dir}")
        
        # Create training info file
        training_info = {
            "run_name": args.run_name,
            "base_model": args.base_model,
            "training_params": {
                "epochs": args.epochs,
                "batch_size": args.batch_size,
                "learning_rate": args.lr,
                "max_seq_len": args.max_seq_len,
                "save_steps": args.save_steps
            },
            "dataset_info": {
                "samples": len(ds),
                "source": args.data
            },
            "completion_time": time.strftime('%Y-%m-%d %H:%M:%S'),
            "model_files": os.listdir(args.output_dir)
        }
        
        info_file = os.path.join(args.output_dir, "training_info.json")
        with open(info_file, "w", encoding="utf-8") as f:
            import json
            json.dump(training_info, f, indent=2, ensure_ascii=False)
        
        # Create compressed archive
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        tar_filename = f"jotica_{args.run_name}_{timestamp}.tar.gz"
        tar_path = os.path.join("/tmp" if os.path.exists("/tmp") else args.output_dir, tar_filename)
        
        print(f"📦 Creating archive: {tar_filename}")
        zip_dir(args.output_dir, tar_path)
        
        # Upload to Supabase with detailed logging
        print("☁️ Uploading to Supabase Storage...")
        upload_result = upload_ckpt(tar_path, prefix=f"{args.run_name}/")
        
        if upload_result.get("success"):
            print("🎉 Checkpoint successfully backed up to Supabase!")
            print(f"   Remote path: {upload_result['remote_path']}")
            print(f"   File size: {upload_result['file_size'] / (1024*1024):.2f} MB")
            
            # Clean up local tar file if upload successful
            try:
                os.remove(tar_path)
                print("🧹 Local archive cleaned up")
            except Exception:
                pass
                
        else:
            print(f"⚠️ Supabase upload failed: {upload_result.get('error')}")
            print(f"   Archive saved locally: {tar_path}")
        
        print("\n✅ Training pipeline completed!")
        print("🔗 Check your models at: https://app.supabase.com/project/jmtrhukymrhzrmqmgrfq/storage/buckets")