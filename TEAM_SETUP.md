# Project Requirements

## Required Software

- Python 3.11.x
- Git
- Visual Studio Code (Recommended)
- GitHub Account

---

# First-Time Setup

## Step 1 - Install Python

Download Python 3.11.x

https://www.python.org/downloads/

Verify installation:

```bash
python --version
```

Expected:

```text
Python 3.11.x
```

---

## Step 2 - Install Git

Download Git:

https://git-scm.com/download/win

Verify installation:

```bash
git --version
```

---

## Step 3 - Accept the GitHub Invitation

Kyle will invite you as a collaborator.

1. Check your email.
2. Accept the GitHub invitation.
3. Verify that you can access the QuantumHPC repository.

---

## Step 4 - Clone the Repository

Open Command Prompt.

Navigate to where you want your projects.

Example:

```bash
cd C:\GitHub
```

Clone the repository:

```bash
git clone https://github.com/kahartne/QuantumHPC.git
```

Move into the project:

```bash
cd QuantumHPC
```

---

## Step 5 - Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it.

Windows:

```bash
.venv\Scripts\activate
```

You should now see:

```text
(.venv)
```

at the beginning of your terminal.

---

## Step 6 - Install Dependencies

```bash
pip install -r requirements.txt
```

If you are working on HPC or MPI components later:

```bash
pip install -r requirements-hpc.txt
```

---

## Step 7 - Verify the Project Runs

```bash
python main.py
```

If everything is configured correctly, the simulator should execute successfully.

---

# Daily Workflow

Every time you begin working:

Activate the virtual environment.

```bash
.venv\Scripts\activate
```

Navigate to the repository.

```bash
cd QuantumHPC
```

Download the latest changes.

```bash
git checkout main
git pull origin main
```

Switch to your development branch.

Example:

```bash
git checkout edmund-quantum
```

or

```bash
git checkout sofia-clinical
```

---

# Making Changes

Edit your code.

Run the project to verify everything still works.

---

# Saving Your Work

See what changed.

```bash
git status
```

Stage your changes.

```bash
git add .
```

Create a commit.

```bash
git commit -m "Brief description of your changes"
```

Push your branch.

```bash
git push origin YOUR_BRANCH_NAME
```

Example:

```bash
git push origin edmund-quantum
```

---

# Creating a Pull Request

After pushing your branch:

1. Open GitHub.
2. Select your branch.
3. Click **Compare & Pull Request**.
4. Add a short description.
5. Submit the Pull Request.

Kyle will review and merge changes into the main branch.

---

# Before Starting New Work

Always update your local copy first.

```bash
git checkout main
git pull origin main
```

Then return to your branch.

```bash
git checkout YOUR_BRANCH_NAME
git merge main
```

This keeps your branch up to date with everyone else's work.

---

# Common Problems

## Git is not recognized

Reinstall Git:

https://git-scm.com/download/win

Restart Command Prompt.

---

## Wrong Python Version

Verify:

```bash
python --version
```

This project currently requires:

```text
Python 3.11.x
```

---

## Virtual Environment Not Active

Activate it again.

```bash
.venv\Scripts\activate
```

---

## Missing Packages

Run:

```bash
pip install -r requirements.txt
```

---

## Merge Conflicts

Stop and ask before resolving merge conflicts if you are unsure.

Do **not** delete another teammate's code.

---

# Team Roles

**Kyle Hartness**
- Repository Maintainer
- HPC Development
- Benchmarking
- MPI
- Performance Analysis

**Edmund**
- Quantum Circuit Development
- Quantum Algorithms
- Feature Maps

**Sofia**
- Clinical Data
- Preprocessing
- Dataset Integration

---

# Repository Rules

- Never commit directly to **main**.
- Always work on your assigned branch.
- Test your code before pushing.
- Write clear commit messages.
- Ask questions if something is unclear.
