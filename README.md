🛡️ Cyber-Sentinel: Inode-Based Virtual File System (VFS)

A high-performance, isolated Virtual File System (VFS) designed to simulate low-level Operating System storage management. This project implements a custom block-based storage engine with a 1MB capacity, offering both a Graphical User Interface (GUI) and a Terminal User Interface (TUI).

## 🏗️ Architecture & Design
The system is built on a custom **Inode-based architecture**, which decouples file metadata from the actual data blocks. 

- **Storage Simulation:** A virtual disk of 1MB ($1,048,576$ bytes) is partitioned into 256 logical blocks of 4KB each.
- **Linked Allocation:** Files are stored across non-contiguous blocks, managed via pointers within the Inode table to prevent external fragmentation.
- **Metadata Management:** Each Inode tracks:
    - File size and block pointers.
    - Permissions (`rw` mode).
    - Timestamps (Created, Modified, Accessed).
- **Persistence:** System state is serialized via JSON into `vfs_state.json`, ensuring data retention across restarts.



## 🚀 Key Features
- **Visual Block Map:** Real-time grid visualization of physical block allocation using PyQt5.
- **Dual-Mode Interface:** - **Dashboard (GUI):** For visual management and storage telemetry.
    - **Engine (TUI):** For command-line operations and low-level testing.
- **Environment Isolation:** Designed to run in a Python Virtual Environment (`venv`) to ensure host system security and dependency integrity.

## 🛠️ Setup & Installation
Follow these steps to deploy the VFS on your local machine or Linux VM:

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/chinmayamr007/File-system-management.git](https://github.com/chinmayamr007/File-system-management.git)
   cd File-system-management

    Initialize Isolated Environment:
    Bash

python3 -m venv venv
source venv/bin/activate

Install Dependencies:
Bash

    pip install PyQt5

💻 Usage
Launching the Dashboard (GUI)
Bash

python3 gui.py

Launching the Terminal Engine (TUI)
Bash

python3 vfs_engine.py

Supported Commands (TUI)
Command	Usage	Description
create	create <file>	Initializes a new Inode in the table
write	write <file> <text>	Allocates blocks and commits data
read	read <file>	Retrieves and assembles data from blocks
delete	delete <file>	Deallocates blocks and wipes the Inode
info	info <file>	Displays detailed metadata JSON
stats	stats	Shows total/used/free block statistics
🎓 Learning Outcomes

    OS Fundamentals: Practical implementation of file systems and linked allocation.

    Data Persistence: Mastery of serialization techniques for system state recovery.

    System Troubleshooting: Configuring display dependencies (XCB/Wayland) in a VMware Linux environment.

Developed by: Chinmaya M R

Specialization: AI & Machine Learning | Cyber Security Intern @ CoE-DFICS


---

### One final step for your Repo:
To make this truly professional, run this command in your terminal to create the `requirements.txt` file we talked about:

```bash
echo "PyQt5" > requirements.txt
git add README.md requirements.txt
git commit -m "Docs: Add detailed README and requirements.txt"
git push
