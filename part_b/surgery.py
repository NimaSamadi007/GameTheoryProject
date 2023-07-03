import numpy as np

class Surgery:
    ID = 1
    # Waiting slot is only used in part b
    def __init__(self, surg_type, ts, pref, waiting_slot):
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
        self.waiting_slot = waiting_slot
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
    
    def proposeOptimal(self):
        if self.waiting_slot > 0:
            # This surgery can wait
            return self.pref[0]
        else:
            # no matter what, must participate
            # in the current cycle
            return None

    def __str__(self):
        return f"{chr(ord('A')+self.surg_type)}({self.ID}) @ {self.creation_time:.3f} # {self.waiting_slot}"
    
    def __repr__(self):
        return str(self)
