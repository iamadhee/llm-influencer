def sanitize_script(script):
    if "```" in script:
        script.replace("```", "")
    if "```python" in script:
        script.replace("```python", "")
    return script
