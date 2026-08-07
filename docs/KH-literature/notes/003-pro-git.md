# 003 – Pro Git

## IEEE Reference

[3] S. Chacon and B. Straub, *Pro Git*, 2nd ed. Apress, 2014. [Online]. Available: https://git-scm.com/book/en/v2. Accessed: Jul. 23, 2026.

---

## Purpose

Primary reference for Git. Integrates external coding with a central GitHub repository.

---

## Summary

Explains Git fundamentals including repositories, commits, branching, merging, remotes, rebasing, and collaborative development.

---

## Important Topics

- Branches
- Merge
- Remote repositories
- Git workflow
- Conflict resolution

---

## Relevance

- Repository management
- Team collaboration
- Version control
- Branch workflow

---

## Personal Notes

- Clone an existing repository: git clone <url>
- Commit changes: git commit -m 'Commit message'
- Check the state of files (untracked vs unmodified vs modified vs staged): git status
- To track specific file: git add <filename>
- To track all files: git add .
- To remove a specific file: git rm <filename>
- To move a specific file: git mv file_from file_to
- Default remote repository: origin
- Push: git push origin <branch>
- Pull: git pull origin <branch>
- Create a branch: git branch <branchname>
- Switch to a branch: git checkout <branch>
- Merge current branch into target branch: git checkout current_branch
                                           git merge target_branch
- There are also a variety of instructions for using GitHub