import os
import json
import time
import math

# Configuration based on PRD
BLOCK_SIZE = 4096  # 4KB 
TOTAL_STORAGE = 1024 * 1024  # 1MB 
TOTAL_BLOCKS = TOTAL_STORAGE // BLOCK_SIZE # 256 Blocks 

class VirtualFileSystem:
    def __init__(self, persistence_file="vfs_state.json"):
        self.persistence_file = persistence_file
        self.storage = [""] * TOTAL_BLOCKS  
        self.inodes = {}  # Inode-based architecture [cite: 8]
        self.load_state() 

    def load_state(self):
        """Restores file system state from disk[cite: 26, 28]."""
        if os.path.exists(self.persistence_file):
            try:
                with open(self.persistence_file, "r") as f:
                    state = json.load(f)
                    self.inodes = state.get("inodes", {})
                    self.storage = state.get("storage", [""] * TOTAL_BLOCKS)
            except Exception:
                pass

    def save_state(self):
        """Serializes inodes and storage for persistence[cite: 27]."""
        state = {"inodes": self.inodes, "storage": self.storage}
        with open(self.persistence_file, "w") as f:
            json.dump(state, f)

    def get_free_blocks(self):
        """Finds available block indices[cite: 9]."""
        return [i for i, block in enumerate(self.storage) if not block]

    def create(self, name):
        """Creates a new file entry[cite: 17, 50]."""
        if name in self.inodes: return f"Error: '{name}' exists."
        self.inodes[name] = {
            "name": name,
            "size": 0,
            "blocks": [],
            "created": time.ctime(),
            "modified": time.ctime(),
            "accessed": time.ctime(),
            "permissions": "rw" # [cite: 54, 55, 56, 57]
        }
        self.save_state()
        return f"File '{name}' created."

    def write(self, name, content):
        """Implements block-based linked allocation[cite: 12, 18]."""
        if name not in self.inodes: return "Error: Not found."
        
        # Free old blocks before writing [cite: 13]
        for b_idx in self.inodes[name]["blocks"]:
            self.storage[b_idx] = ""
            
        needed = math.ceil(len(content) / BLOCK_SIZE)
        free_indices = self.get_free_blocks()
        
        if len(free_indices) < needed:
            return "Error: Storage full (1MB limit)."

        allocated = free_indices[:needed]
        for i, b_idx in enumerate(allocated):
            self.storage[b_idx] = content[i*BLOCK_SIZE : (i+1)*BLOCK_SIZE]
        
        self.inodes[name]["blocks"] = allocated 
        self.inodes[name]["size"] = len(content)
        self.inodes[name]["modified"] = time.ctime()
        self.save_state()
        return f"Wrote {len(content)} bytes."

    def read(self, name):
        """Reads content from logical blocks[cite: 19]."""
        if name not in self.inodes: return "Error: Not found."
        content = "".join([self.storage[b] for b in self.inodes[name]["blocks"]])
        self.inodes[name]["accessed"] = time.ctime()
        self.save_state()
        return content

    def delete(self, name):
        """Deallocates blocks and removes inode[cite: 13, 20]."""
        if name not in self.inodes: return "Error: Not found."
        for b_idx in self.inodes[name]["blocks"]:
            self.storage[b_idx] = ""
        del self.inodes[name]
        self.save_state()
        return f"File '{name}' deleted."

    def get_stats(self):
        """Returns block usage statistics[cite: 34, 45]."""
        used = sum(1 for b in self.storage if b)
        return {"total_blocks": TOTAL_BLOCKS, "used_blocks": used, "free_blocks": TOTAL_BLOCKS - used}

def run_tui():
    """Terminal User Interface Command Loop[cite: 37]."""
    vfs = VirtualFileSystem()
    print("🛡️ Virtual File System TUI Active")
    print("Commands: create, write, read, delete, list, info, stats, exit")
    
    while True:
        try:
            line = input("fs> ").strip().split(maxsplit=2)
            if not line: continue
            cmd = line[0].lower()
            
            if cmd == "exit": break # [cite: 47]
            elif cmd == "create": print(vfs.create(line[1])) # [cite: 38]
            elif cmd == "write": print(vfs.write(line[1], line[2])) # [cite: 39]
            elif cmd == "read": print(vfs.read(line[1])) # [cite: 40]
            elif cmd == "delete": print(vfs.delete(line[1])) # [cite: 41]
            elif cmd == "list": print("\n".join(vfs.inodes.keys())) # [cite: 43]
            elif cmd == "info": # [cite: 44]
                print(json.dumps(vfs.inodes.get(line[1], "Not found"), indent=2))
            elif cmd == "stats": print(vfs.get_stats()) # [cite: 45]
            else: print("Unknown command.")
        except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    run_tui()
