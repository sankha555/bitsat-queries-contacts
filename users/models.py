from django.db import models
from django.contrib.auth.models import User
from hashlib import sha1

branches = {
    "A1": "B.E. Chemical",
    "A2": "B.E. Civil",
    "A3": "B.E. Electrical and Electronics (EEE)",
    "A4": "B.E. Mechanical",
    "A5": "B.Pharm",
    "A7": "B.E. Computer Science",
    "A8": "B.E. Electronics and Instrumentation (ENI)",
    "AA": "B.E. Electronics and Communication (ECE)",
    "AB": "B.E. Manufacturing",
    
    "B1": "M.Sc. Biology",
    "B2": "M.Sc. Chemistry",
    "B3": "M.Sc. Economics",
    "B4": "M.Sc. Mathematics",
    "B5": "M.Sc. Physics",
    
    "D2": "M.Sc. General Studies"
}

class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField("Name", max_length=200, null=True, blank=True)
    bits_id = models.CharField("BITS ID", max_length=50, null=True, blank=True)
    bits_email = models.CharField("BITS Email", max_length=50, null=True, blank=True)
    
    batch = models.CharField("Admission Batch", max_length=50, null=True, blank=True)
    year = models.IntegerField("Year", default=1)
    campus = models.CharField("Campus", max_length=50, null=True, blank=True)
    branch1 = models.CharField("B.E. Branch", max_length=50, null=True, blank=True)    # BE branch code
    branch2 = models.CharField("M.Sc. Branch", max_length=50, null=True, blank=True)   # MSc branch code
    branch_string = models.CharField("Branch", max_length=100, null=True, blank=True)
    is_dualite = models.BooleanField("Is Dualite", default=False, null=True, blank=True)
    
    phone_number = models.CharField("Phone Number", max_length=50, null=True, blank=True)
    fb_profile = models.CharField("Facebook Profile Link", max_length=1000, null=True, blank=True)
    
    contact_regarding = models.TextField("You can contact the student regarding", max_length=5000, null=True, blank=True)
    contact_time = models.TextField("You can contact the student at this time", max_length=5000, null=True, blank=True)
    
    student_slug = models.CharField("Student slug", max_length=50, null=True, blank=True)
    
    private_mode = models.BooleanField("Private Mode", default = False)
    
    def calculate_student_slug(self):
        bits_id = self.bits_id
        id_hash = sha1(bits_id.encode("utf-8")).hexdigest()
        self.student_slug = (id_hash[::-1])[:10]
    
    def extract_branches(self):
        bits_id = self.bits_id
        self.calculate_student_slug()
        
        try:
            if bits_id[0] == "F":
                bits_id = bits_id[1:]
            
            if bits_id[:2] != "20":
                bits_id = "20" + bits_id
            
            # 2019A7PS0029P
            if bits_id[6:8] == "PS" or bits_id[6:8] == "TS":
                self.is_dualite = False
                self.branch2 = "";
                self.branch1 = bits_id[4:6]
                
                try:
                    self.branch_string = branches[bits_id[4:6]]
                except:
                    pass
            else:
                self.is_dualite = True
                self.branch2 = bits_id[4:6]
                self.branch1 = bits_id[6:8]
                
                try:
                    self.branch_string = branches[bits_id[4:6]] + " + " + branches[bits_id[6:8]]
                except:
                    pass
            
            self.batch = bits_id[:4]
            self.year = 2021 - int(bits_id[:4]) + 1
            
            phone_number = str(self.phone_number )
            if phone_number != "" and len(phone_number) > 2:
                if phone_number[-2] == ".":
                    phone_number = phone_number[:-2]
                    self.phone_number = phone_number
            
        except:
            pass
        
    def __str__(self):
        return self.name
    
class Aspirant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField("Name", max_length=200, null=True, blank=True)
    