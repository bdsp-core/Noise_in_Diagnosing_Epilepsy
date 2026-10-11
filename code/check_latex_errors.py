#!/usr/bin/env python3
"""
Check for common LaTeX compilation errors in kilt.tex
"""

import re

def check_latex_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    errors = []
    warnings = []

    # Track environment nesting
    env_stack = []

    # Track math mode
    in_display_math = False
    in_inline_math = False

    for i, line in enumerate(lines, 1):
        # Check for unmatched environments
        begin_matches = re.findall(r'\\begin\{([^}]+)\}', line)
        end_matches = re.findall(r'\\end\{([^}]+)\}', line)

        for env in begin_matches:
            env_stack.append((env, i))

        for env in end_matches:
            if not env_stack:
                errors.append(f"Line {i}: Unmatched \\end{{{env}}}")
            elif env_stack[-1][0] != env:
                errors.append(f"Line {i}: Mismatched environment - expected \\end{{{env_stack[-1][0]}}}, got \\end{{{env}}}")
            else:
                env_stack.pop()

        # Check for $$ (discouraged in LaTeX)
        if '$$' in line and not line.strip().startswith('%'):
            warnings.append(f"Line {i}: Found $$ (consider using \\[ \\] instead)")

        # Check for unescaped special characters (basic check)
        if not line.strip().startswith('%'):
            # Check for & outside math/tabular
            if '&' in line and not any(env[0] in ['eqnarray', 'align', 'aligned', 'tabular', 'array'] for env in env_stack):
                if '\\&' not in line:
                    warnings.append(f"Line {i}: Possible unescaped & outside math/tabular")

        # Check for unclosed braces (simple check)
        open_braces = line.count('{') - line.count('\\{')
        close_braces = line.count('}') - line.count('\\}')
        if open_braces != close_braces:
            warnings.append(f"Line {i}: Unbalanced braces (open={open_braces}, close={close_braces})")

    # Check for unclosed environments
    if env_stack:
        for env, line_num in env_stack:
            errors.append(f"Line {line_num}: Unclosed \\begin{{{env}}}")

    print("="*60)
    print("LaTeX Error Check Results")
    print("="*60)

    if errors:
        print(f"\n{len(errors)} ERRORS found:")
        for error in errors[:20]:  # Show first 20
            print(f"  ❌ {error}")
        if len(errors) > 20:
            print(f"  ... and {len(errors)-20} more")
    else:
        print("\n✅ No critical errors found")

    if warnings:
        print(f"\n{len(warnings)} WARNINGS:")
        for warning in warnings[:20]:  # Show first 20
            print(f"  ⚠️  {warning}")
        if len(warnings) > 20:
            print(f"  ... and {len(warnings)-20} more")
    else:
        print("\n✅ No warnings")

    print("\n" + "="*60)
    return len(errors) == 0

if __name__ == "__main__":
    import sys
    filename = "/Users/bwestove/cdac Dropbox/brandon westover/0_People/temp_people/fabio/KILT_technical/Noise_in_Diagnosing_Epilepsy/kilt.tex"
    success = check_latex_file(filename)
    sys.exit(0 if success else 1)
