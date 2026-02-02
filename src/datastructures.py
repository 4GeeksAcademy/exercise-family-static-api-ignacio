class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._next_id = 1
        self._members = []
    
    def _generate_id(self):
        generated_id = self._next_id
        self._next_id += 1
        return generated_id

    def add_member(self, member):
        try:
            if "id" in member:
                existing_ids = [m["id"] for m in self._members]
                if member["id"] in existing_ids:
                    pass
            else:
                member["id"] = self._generate_id()
            if "lucky_numbers" in member:
                if isinstance(member["lucky_numbers"], list):
                    member["lucky_numbers"] = list(member["lucky_numbers"])
                else:
                    member["lucky_numbers"] = []
            else:
                member["lucky_numbers"] = []
            member["last_name"] = self.last_name
            
            self._members.append(member)
            return member
            
        except Exception as e:
            print(f"Error adding member: {e}")
            return None
    
    def delete_member(self, id):
        for position in range(len(self._members)):
            if self._members[position]["id"] == id:
                self._members.pop(position)
                return {"done": True}
        return None
    
    def get_member(self, id):
        for member in self._members:
            if member["id"] == int(id):
                return member
        return None
    
    def get_all_members(self):
        return self._members