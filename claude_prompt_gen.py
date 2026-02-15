#!/usr/bin/env python3
"""
Claude Prompt Generator - Generate CLAUDE.md files for Cline projects.

Usage:
    claude_prompt_gen.py --name "My Project" --lang python --framework fastapi

Creates a CLAUDE.md file with project-specific instructions.
"""

import sys
from pathlib import Path

PYTHON_PROMPTS = {
    "framework": "You are an expert Python developer. Follow PEP 8 style guidelines.",
    "test": "Write tests using pytest. Ensure 80% code coverage.",
    "doc": "Include docstrings for all functions and classes.",
}

JS_PROMPTS = {
    "framework": "You are an expert JavaScript/TypeScript developer. Follow modern ES6+ patterns.",
    "test": "Write tests using Jest. Follow TDD principles.",
    "doc": "Include JSDoc comments for all functions.",
}

LANGUAGES = {
    "python": PYTHON_PROMPTS,
    "javascript": JS_PROMPTS,
    "typescript": JS_PROMPTS,
}

DEFAULT_PROMPT = """# Claude Instructions

You are an expert software developer. Follow these guidelines:
- Write clean, maintainable code
- Include appropriate comments
- Consider security best practices
- Write tests for your code
"""

def generate_prompt(name: str, language: str = None, framework: str = None,
                   include_tests: bool = True, include_docs: bool = True) -> str:
    """Generate a CLAUDE.md file."""
    
    prompt = f"""# Project: {name}

{DEFAULT_PROMPT}
"""
    
    if language and language in LANGUAGES:
        prompt += f"\n## Language\n\n{LANGUAGES[language].get('framework', '')}\n"
    
    if include_tests:
        prompt += "\n## Testing\n\n"
        if language:
            prompt += f"{LANGUAGES[language].get('test', '')}\n"
        else:
            prompt += "Write comprehensive tests for all features.\n"
    
    if include_docs:
        prompt += "\n## Documentation\n\n"
        if language:
            prompt += f"{LANGUAGES[language].get('doc', '')}\n"
        else:
            prompt += "Document all public APIs and complex logic.\n"
    
    if framework:
        prompt += f"\n## Framework\n\nUsing {framework}. Follow framework-specific best practices.\n"
    
    return prompt

def main():
    if len(sys.argv) < 2:
        print("Usage: claude_prompt_gen.py --name <project> [--lang python|javascript|typescript] [--framework <name>] [--no-tests] [--no-docs]")
        print("\nExamples:")
        print("  claude_prompt_gen.py --name 'API' --lang python --framework fastapi")
        print("  claude_prompt_gen.py --name 'WebApp' --lang typescript --framework react")
        sys.exit(1)
    
    name = None
    language = None
    framework = None
    include_tests = True
    include_docs = True
    
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--name" and i + 1 < len(sys.argv):
            name = sys.argv[i + 1]
            i += 2
        elif arg == "--lang" and i + 1 < len(sys.argv):
            language = sys.argv[i + 1]
            i += 2
        elif arg == "--framework" and i + 1 < len(sys.argv):
            framework = sys.argv[i + 1]
            i += 2
        elif arg == "--no-tests":
            include_tests = False
            i += 1
        elif arg == "--no-docs":
            include_docs = False
            i += 1
        else:
            i += 1
    
    if not name:
        print("Error: --name is required")
        sys.exit(1)
    
    prompt = generate_prompt(name, language, framework, include_tests, include_docs)
    
    # Write to CLAUDE.md
    output_path = Path.cwd() / "CLAUDE.md"
    with open(output_path, 'w') as f:
        f.write(prompt)
    
    print(f"✓ Created CLAUDE.md for '{name}'")
    if language:
        print(f"  Language: {language}")
    if framework:
        print(f"  Framework: {framework}")
    print(f"  Tests: {include_tests}")
    print(f"  Docs: {include_docs}")

if __name__ == "__main__":
    main()
