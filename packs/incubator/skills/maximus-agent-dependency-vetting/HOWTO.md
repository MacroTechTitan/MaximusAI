# HOWTO — Agent Dependency Vetting

## 1. Check one package before an agent installs it
`python examples/vet_package.py pypi aws-cdk` or `python examples/vet_package.py npm left-pad`. Exit code 0 means allow, 1 means hold for review, 2 means block. Wire it in as the agent's required pre-install step, or a hook that runs before any `pip install`, `npm install`, or `npx`.

## 2. npm project defaults
Copy `examples/npmrc.example` to `.npmrc`: scripts off by default, a 7-day release-age window, and an exemption list. Turn scripts on per package only when a build needs them.

## 3. Python project defaults
With uv, add `exclude-newer = "7 days"` under `[tool.uv]` and use `exclude-newer-package` for exemptions. With pip, generate a hashed lock (`pip-compile --generate-hashes`) and deploy with `pip install --require-hashes -r requirements.txt`.

## 4. Review rule for new names
Add a CODEOWNERS entry or branch rule that requires a human reviewer on changes to `package.json`, lock files, `requirements*.txt`, and `pyproject.toml`. In the PR, paste the vet output for every new name.

## 5. Audit an existing repository or copied skill pack
Extract every install command and import, then run the vetter over the names. Pay special attention to agent skill files and templates copied from other repositories.
