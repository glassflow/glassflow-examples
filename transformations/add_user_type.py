
def handler(data, log):
    user_id = data.get('user_id', '')
    # Assume a function getUserType returns user type based on user_id
    data['user_type'] = getUserType(user_id)
    return data

def getUserType(user_id):
    user_types = {
        '001': 'Admin',
        '002': 'Editor',
        '003': 'Viewer',
        # Add more mappings as needed
    }
    return user_types.get(user_id, 'Guest')
    