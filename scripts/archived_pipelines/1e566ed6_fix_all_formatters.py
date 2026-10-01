import os

def main():
    scratch_dir = r"C:\Users\augus\.\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch"
    # Resolve relative parts
    scratch_dir = os.path.abspath(scratch_dir)
    
    scripts = [
        "faithful_format_part1.py",
        "format_part2.py",
        "format_part3.py",
        "format_part4.py",
        "format_part5.py",
        "format_appendix.py",
        "format_glossary.py"
    ]
    
    for filename in scripts:
        path = os.path.join(scratch_dir, filename)
        if not os.path.exists(path):
            print(f"Skipping (not found): {filename}")
            continue
            
        with open(path, 'r', encoding='utf-8') as f:
            code = f.read()
            
        # 1. Replace the newline normalization line
        old_normalizer = "content = content.replace('\\r\\n', '\\n').replace('\\n', '\\r\\n')"
        new_normalizer = "content = content.replace('\\r\\n', '\\n')"
        code = code.replace(old_normalizer, new_normalizer)
        
        # 2. Replace write file line to use newline='\n'
        old_writer = "with open(target_path, 'w', encoding='utf-8') as f:"
        new_writer = "with open(target_path, 'w', encoding='utf-8', newline='\\n') as f:"
        code = code.replace(old_writer, new_writer)
        
        # 3. Specific adjustments per script
        if filename == "faithful_format_part1.py":
            # Normalize replacements list to use \n in both orig and rep
            normalizer_inject = "\nreplacements = [(orig.replace('\\r\\n', '\\n'), rep.replace('\\r\\n', '\\n')) for orig, rep in replacements]\n"
            if "mismatches = 0" in code and normalizer_inject not in code:
                code = code.replace("mismatches = 0", normalizer_inject + "mismatches = 0")
                
        elif filename == "format_part3.py":
            # Normalize dialogue vars before replacements
            vars_to_normalize = [
                "dialogue_252_form", "dialogue_259_form", "dialogue_788_form",
                "dialogue_792_form1", "dialogue_792_form2", "dialogue_812_form",
                "dialogue_879_form", "dialogue_1334_form", "dialogue_1335_form",
                "dialogue_1337_form"
            ]
            normalization_lines = "\n# Normalize dialogue forms to Unix newlines\n"
            for v in vars_to_normalize:
                normalization_lines += f"{v} = {v}.replace('\\r\\n', '\\n')\n"
            
            # Inject before the first dialogue replacement
            if "content = content.replace(dialogue_252_orig" in code:
                code = code.replace(
                    "content = content.replace(dialogue_252_orig",
                    normalization_lines + "\ncontent = content.replace(dialogue_252_orig"
                )
                
        elif filename == "format_part4.py":
            # Normalize dialogue vars before replacements
            vars_to_normalize = [
                "dialogue_118_form", "dialogue_232_form", "dialogue_273_form",
                "dialogue_304_form", "dialogue_469_form", "dialogue_547_form",
                "dialogue_567_form", "dialogue_602_form", "dialogue_637_form",
                "dialogue_642_form"
            ]
            normalization_lines = "\n# Normalize dialogue forms to Unix newlines\n"
            for v in vars_to_normalize:
                normalization_lines += f"{v} = {v}.replace('\\r\\n', '\\n')\n"
                
            # Inject before the first dialogue replacement in part 4
            if "content = content.replace(dialogue_118_orig" in code:
                code = code.replace(
                    "content = content.replace(dialogue_118_orig",
                    normalization_lines + "\ncontent = content.replace(dialogue_118_orig"
                )
                
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(code)
            
        print(f"Successfully patched {filename}")

if __name__ == "__main__":
    main()
