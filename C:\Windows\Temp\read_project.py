
import os

base_path = r"E:\ai_test_MedGemma\ai\other"

files_to_read = [
    "MedGemma_4B_全流程说明图.md",
    "MedGemma_DR金标准_标准_v5.0.md",
    "项目实施指导书.md"
]

output_lines = []

for filename in files_to_read:
    filepath = os.path.join(base_path, filename)
    if os.path.isfile(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            output_lines.append(f"\n{'='*60}")
            output_lines.append(f"FILE: {filename}")
            output_lines.append(f"{'='*60}")
            output_lines.append(content[:5000])
        except Exception as e:
            output_lines.append(f"Error reading {filename}: {e}")

with open(r"C:\Windows\Temp\project_summary.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))
