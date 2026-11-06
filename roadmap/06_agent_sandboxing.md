# 06: Zero-Trust Agent Sandboxing & Execution Security

Giving an autonomous AI coding agent unrestricted access to the terminal (`bash`) is an invitation to disaster. 

---

## 1. Why Application-Level Rules Fail

Many systems attempt to constrain agents using prompt directives:
> *"Please do not modify files outside this project directory."*

This fails catastrophically for three reasons:
1. **Prompt Injections & Poisoned Dependencies**: A malicious npm or cargo dependency can inject shell commands via build scripts (`build.rs`, `postinstall`).
2. **Accidental Hallucination**: An LLM agent attempting to clean up a cache might execute `rm -rf /` or `chmod -R 777 ~`.
3. **Network Exfiltration**: A tool can curl sensitive host credentials (`~/.ssh/id_rsa`, `~/.aws/credentials`) to a command-and-control server.

---

## 2. The Zero-Trust Kernel Sandbox Paradigm

Zero-Trust means **never trust the prompt, never trust the LLM, verify in the Linux kernel**.

```
+-------------------------------------------------------------------+
|                        HOST SYSTEM                                |
|                                                                   |
|   +-----------------------------------------------------------+   |
|   |                    SHADOWCLI SANDBOX                      |   |
|   |                                                           |   |
|   |   +--------------------+         +--------------------+   |   |
|   |   | User Namespace     |         | Mount Namespace    |   |   |
|   |   | (CLONE_NEWUSER)    |         | (Private Tmpfs)    |   |   |
|   |   +--------------------+         +--------------------+   |   |
|   |              |                             |              |   |
|   |              v                             v              |   |
|   |   +--------------------+         +--------------------+   |   |
|   |   | Landlock LSM       |         | Network Namespace  |   |   |
|   |   | (Mandatory Access) |         | (Egress Blocked)   |   |   |
|   |   +--------------------+         +--------------------+   |   |
|   |              |                             |              |   |
|   |              v                             v              |   |
|   |   +---------------------------------------------------+   |   |
|   |   | Ephemeral OverlayFS / CopyFS (Upperdir Staging)   |   |   |
|   |   +---------------------------------------------------+   |   |
|   +-----------------------------------------------------------+   |
|                                |                                  |
|                                v                                  |
|           Cryptographic Review Hash (SHA-256)                     |
|                                |                                  |
|                                v                                  |
|           Human Developer Terminal Approval Required              |
+-------------------------------------------------------------------+
```

---

## 3. The 5 Core Principles of Agent Sandboxing

Implemented natively in [ShadowCLI](https://github.com/6t9xstar/shadowcli):

1. **Ephemeral Staging (Copy-on-Write)**: Commands execute in an isolated `upperdir`. The real host project is never mutated during runtime.
2. **Network Egress Denial**: Network namespace (`CLONE_NEWNET`) blocks socket creation by default.
3. **Transient Masking of $HOME**: The user's home directory is masked by an in-memory `tmpfs`. Package caches (`.cargo`, `.rustup`) are mounted strictly read-only.
4. **Landlock LSM Enforcement**: Enforces unbypassable kernel barriers at the VFS layer.
5. **Human Approval Gate**: Staged diffs generate a deterministic SHA-256 review hash. Changes can only be applied to the host by the human developer in their terminal.

---

## Summary
AI Engineering is not just about prompt templates—it is about robust systems engineering, rigorous evaluations, and fail-closed security.
