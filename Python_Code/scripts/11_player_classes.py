


class Player:

    '''
    create a class for a player
    '''
    
    def __init__(self, DOB, region, role, team):

        self.DOB = DOB
        self.region = region
        self.role = role
        self.team = team


faker = Player('07/21/1998', 'KR', 'Mid', 'T1')

print(faker.region)