import numpy as np

class Hospital:
    def __init__(self, hosp_type, pref):
        """
        pref: Preference over surgeries
        (price) [(0) 'A', (1) 'B', (2) 'C']
        """
        self.hosp_type = hosp_type
        # sorted in ascending order
        self.pref = pref
        self.revenue = np.zeros(3, dtype=float)
        self.surg_time = np.zeros(3, dtype=float)
        self.num_surg = np.zeros(3, dtype=int)

        self.empty = True
        self.matched = False
        self.matched_surg = None # index of matched surgery
        self.remain_time = 0
    
    def evaluate(self, new_surg):
        if not self.empty:
            # Hospital is not empty, unable to accept proposal
            return False
        if not self.matched:
            self.matched = True
            return True
        else:
            # Evaluate new proposal
            pre_price_ind = self.matched_surg.surg_type
            new_price_ind = new_surg.surg_type
            if self.pref[new_price_ind] > self.pref[pre_price_ind]:
                # this match is strcitly prefered
                self.matched_surg.assigned = False
                self.matched_surg.matched_hospital = None
                self.matched_surg = None
                self.matched = True
                return True
            elif self.pref[new_price_ind] == self.pref[pre_price_ind]:
                # same type, compare creation time
                if self.matched_surg.creation_time > new_surg.creation_time:
                    # new surgery created sooner
                    self.matched_surg.assigned = False
                    self.matched_surg.matched_hospital = None
                    self.matched_surg = None
                    self.matched = True
                    return True
                else:
                    return False
            else:
                return False
    
    def assign(self, surg):
        self.matched = True
        self.matched_surg = surg
        self.matched_surg.assigned = True
        self.matched_surg.matched_hospital = self
    
    def clear(self):
        self.matched = False
        self.matched_surg = None
        self.empty = True
        self.remain_time = 0
        
    def __str__(self):
        return f"{chr(self.hosp_type+ord('a'))}"
    
    def __repr__(self):
        return str(self)
    