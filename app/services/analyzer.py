import os
import shutil
import tempfile
from radon.complexity import cc_visit
from radon.metrics import mi_visit
import subprocess

def clone_repo(repo_url):
    """Clone a github repo into a temp directory and return the path"""
    temp_dir = tempfile.mkdtemp()
    try:
        import git
        git.Repo.clone_from(repo_url, temp_dir)
        return temp_dir
    except Exception as e:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise Exception(f"Failed to clone repo: {str(e)}")

def get_python_files(directory):
    """Get all python files in a directory"""
    python_files = []
    for root, dirs, files in os.walk(directory):
        # Skip hidden directories and common non-source dirs
        dirs[:] = [d for d in dirs if not d.startswith('.') 
                   and d not in ['venv', 'env', '__pycache__', 'node_modules']]
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

def analyze_complexity(python_files):
    """Run radon complexity analysis on all python files"""
    total_complexity = 0
    total_functions = 0

    for filepath in python_files:
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                code = f.read()
            results = cc_visit(code)
            for block in results:
                total_complexity += block.complexity
                total_functions += 1
        except Exception:
            continue

    if total_functions == 0:
        return 0.0

    return round(total_complexity / total_functions, 2)

def analyze_pylint(directory):
    """Run pylint on the directory and return score, warnings, errors"""
    try:
        result = subprocess.run(
            ['pylint', directory, '--output-format=text', '--score=y'],
            capture_output=True,
            text=True
        )
        output = result.stdout + result.stderr

        score = 0.0
        warnings = 0
        errors = 0

        for line in output.split('\n'):
            if 'rated at' in line:
                try:
                    part = line.split('rated at')[1]
                    score = float(part.split('/')[0].strip())
                except:
                    score = 0.0
            if ': W' in line:
                warnings += 1
            if ': E' in line:
                errors += 1

        return round(score, 2), warnings, errors

    except Exception as e:
        print(f"Pylint error: {str(e)}")
        return 0.0, 0, 0

def analyze_repo(repo_url):
    """Main function - clone repo, run all analysis, return results"""
    temp_dir = None
    try:
        temp_dir = clone_repo(repo_url)
        python_files = get_python_files(temp_dir)

        if not python_files:
            raise Exception("No Python files found in repository")

        complexity = analyze_complexity(python_files)
        pylint_score, warnings, errors = analyze_pylint(temp_dir)

        return {
            "complexity_score": complexity,
            "pylint_score": pylint_score,
            "pylint_warnings": warnings,
            "pylint_errors": errors
        }
    finally:
        if temp_dir:
            shutil.rmtree(temp_dir, ignore_errors=True)