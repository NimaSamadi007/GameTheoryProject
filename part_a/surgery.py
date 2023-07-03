import numpy as np

class Surgery:
    ID = 1
    # Waiting slot is only used in part b
    def __init__(self, surg_type, ts, pref):
        """
        pref: Preference over hospitals
        (surgery time) [(0) 'a', (1) 'b', (2) 'c']
        """
        self.surg_type = surg_type
        # sorted in descending order
        self.all_surg_time = np.sort(pref)
        self.pref = np.argsort(pref)
        self.compl_time = 0
        self.creation_time = ts
        self.serve_time = 0
        # corresponding to ['a', 'b', 'c']
        self.proposed = [False, False, False]
        self.matched_hospital = None
        self.assigned = False
        self.ID = Surgery.ID
        Surgery.ID += 1

    def propose(self):
        for prf in self.pref:
            if not self.proposed[prf]:
                # propose to prf
                self.proposed[prf] = True
                return prf
        return None
    
    def __str__(self):
        return f"{chr(ord('A')+self.surg_type)}({self.ID}) @ {self.creation_time:.3f}"
    
    def __repr__(self):
        return str(self)
