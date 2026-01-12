pages = [4, 0, 8, 2, 0, 3, 0, 5, 2, 3, 0, 3, 2]

frame_size = 3


def print_table(rows, title):
    line = "-" * 49 
    print("\n" + title)
    print(line)
    print(f"| {'Step':^6} | {'Page':^6} | {'Frames':^15} | {'Status':^9} |")
    print(line)
    for r in rows:
        # gabungkan frame jadi format [a, b, c]
        frames_str = f"[{r['f1']}, {r['f2']}, {r['f3']}]"
        print(f"| {r['step']:^6} | {r['page']:^6} | {frames_str:^15} | {r['status']:^9} |")
    print(line)


def fifo(pages, frame_size):
    frames = []         
    index_fifo = 0     
    faults = 0         
    hits = 0           
    rows = []          

    for step, page in enumerate(pages, start=1):

        if page in frames:
            status = "HIT"
            hits += 1

        else:
            status = "Fault"
            faults += 1

            if len(frames) < frame_size:
                frames.append(page)

            else:
                frames[index_fifo] = page
                index_fifo = (index_fifo + 1) % frame_size  

        show = frames + ["-"] * (frame_size - len(frames))

        rows.append({
            "step": step,
            "page": page,
            "f1": show[0],
            "f2": show[1],
            "f3": show[2],
            "status": status
        })

    print_table(rows, "=== SIMULASI ALGORITMA FIFO ===")
    print(f"Total Page HIT   = {hits}")
    print(f"Total Page FAULT = {faults}")
    return faults


def lru(pages, frame_size):
    frames = []         
    last_used = {}      
    faults = 0
    hits = 0
    rows = []

    for step, page in enumerate(pages, start=1):

        if page in frames:
            status = "HIT"
            hits += 1

        else:
            status = "Fault"
            faults += 1

           
            if len(frames) < frame_size:
                frames.append(page)

            
            else:
                lru_page = min(last_used, key=last_used.get)  
                frames[frames.index(lru_page)] = page         
                del last_used[lru_page]                       

        last_used[page] = step

        show = frames + ["-"] * (frame_size - len(frames))

        rows.append({
            "step": step,
            "page": page,
            "f1": show[0],
            "f2": show[1],
            "f3": show[2],
            "status": status
        })

    print_table(rows, "=== SIMULASI ALGORITMA LRU ===")
    print(f"Total Page HIT   = {hits}")
    print(f"Total Page FAULT = {faults}")
    return faults

print("PROGRAM SIMULASI PAGE REPLACEMENT: FIFO & LRU")
print("Reference String :", pages)
print("Jumlah Frame     :", frame_size)

fifo_faults = fifo(pages, frame_size)

lru_faults = lru(pages, frame_size)

print("\n=== HASIL ===")
print(f"Total Page Fault Algoritma FIFO : {fifo_faults}")
print(f"Total Page Fault Algoritma LRU  : {lru_faults}")
