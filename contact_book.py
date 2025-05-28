import csv
import os

def divider():
    print('\n-------------------------------------------------\n')

def load_from_csv():
  data = []
  filename = 'data/contacts.csv'
  file_exists = os.path.isfile(filename) and os.path.getsize(filename) > 0
  if not file_exists:
    return data
  with open(filename, mode='r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
      data.append(dict(row))
  return data

def save_in_csv(contacts, mode):
    filename = 'data/contacts.csv'
    if not contacts:
        return
    
    file_exists = os.path.isfile(filename) and os.path.getsize(filename) > 0
    
    with open(filename, mode, newline='') as file:
        writer = csv.DictWriter(file, fieldnames=contacts[0].keys())
        if mode == 'w' or (mode == 'a' and not file_exists):
            writer.writeheader()
        writer.writerows(contacts)

def add_contact():
    new_contact = dict()
    new_contact['name'] = ''
    while(new_contact['name'] == ''):
        new_contact['name'] = input('Contact Name (Required): ')
        
    new_contact['email'] = ''
    while(new_contact['email'] == ''):
        new_contact['email'] = input('Email (Required): ')
        
    new_contact['phone'] = ''
    while(new_contact['phone'] == ''):
        new_contact['phone'] = input('Phone Number (Required): ')
    
    save_in_csv([new_contact], 'a')
    print('\nContact Added Successfully!')
    divider()
    main()

def view_contacts(contacts):
    if not len(contacts)>0:
        print('No Contacts Found\n')
        
    for ind, contact in enumerate(contacts):
        print(f'Contact {ind+1}:\nName: {contact["name"]}\nEmail: {contact["email"]}\nPhone Number: {contact["phone"]}\n')
    divider()
    main()

def search_contact_by_name(contacts):
    isExist = False
    search_name = input('Enter contact name to search: ')
    i = 1
    for contact in contacts:
        if search_name.lower() in str(contact['name']).lower():
            print(f'\nContact {i}:\nName: {contact["name"]}\nEmail: {contact["email"]}\nPhone Number: {contact["phone"]}\n')
            isExist = True
            i+=1     
    if not isExist:
        print('\nNo Result Found')
    divider()
    main()

def update_contact(contacts):
    if not contacts:
        print('\nNo contacts to update. Please add contacts first.')
        divider()
        main()
        return
        
    email_to_update = input('Enter the email of the contact you want to update: ')
    isExist = any(contact['email'] == email_to_update for contact in contacts)
    
    if not isExist:
        print('\nNo contact found with that email.')
        divider()
        main()
        return
    
    menu_for_update = ['Contact Name', 'Email', 'Phone Number', 'Back']
    for i, opt in enumerate(menu_for_update):
        print(f'{i+1}. {opt}')
    print()
    
    selected_opt_update = input('Enter option number for the field you want to update: ')
    
    field_mapping = {
        '1': 'name',
        '2': 'email',
        '3': 'phone'
    }
    
    if selected_opt_update in field_mapping:
        field = field_mapping[selected_opt_update]
        
        for contact in contacts:
            if contact['email'] == email_to_update:
                print('\nUpdating Contact:')
                print(f'Name: {contact["name"]}\nEmail: {contact["email"]}\nPhone Number: {contact["phone"]}\n')
                
                updated_value = ''
                prompt_text = f'Enter new {menu_for_update[int(selected_opt_update)-1]} (Required): '
                
                while updated_value == '':
                    updated_value = input(prompt_text)
                    if updated_value == '':
                        print("This field cannot be empty! Please enter a value.")
                
                contact[field] = updated_value
                
                print('\nContact Updated Successfully!')
                break
        
        save_in_csv(contacts, 'w')
    elif selected_opt_update == '4':
        print('\nReturning to main menu...')
    else:
        print('\nInvalid option selected.')
    
    divider()
    main()

def delete_contact(contacts):
    if not contacts:
        print('\nNo contacts to delete. Please add contacts first.')
        divider()
        main()
        return
        
    email_to_delete = input('Enter the email of the contact you want to delete: ')
    
    contact_to_delete = None
    for contact in contacts:
        if contact['email'] == email_to_delete:
            contact_to_delete = contact
            break
    
    if not contact_to_delete:
        print('\nNo contact found with that email.')
    else:
        print('\nContact to delete:')
        print(f'Name: {contact_to_delete["name"]}\nEmail: {contact_to_delete["email"]}\nPhone Number: {contact_to_delete["phone"]}\n')
        
        confirm = input('Are you sure you want to delete this contact? (yes/no): ')
        
        if confirm.lower() == 'yes':
            contacts.remove(contact_to_delete)
            
            save_in_csv(contacts, 'w')
            print('\nContact Deleted Successfully!')
        else:
            print('\nDeletion cancelled.')
    
    divider()
    main()

def main():
    contacts = load_from_csv()
    selected_opt = input('Option no which action you want to perform: ')

    divider()
    if selected_opt.isnumeric() and int(selected_opt) > 0 and int(selected_opt) <= 6:
        if selected_opt == '1':    
            add_contact()
        elif selected_opt == '2':
            view_contacts(contacts)
        elif selected_opt == '3':
            search_contact_by_name(contacts)
        elif selected_opt == '4':
            update_contact(contacts)
        elif selected_opt == '5':
            delete_contact(contacts)
        elif selected_opt == '6':
            print('Thank you for using Contact Book!')
            quit()
    else:
        print('Invalid Option!')
        divider()
        main()

os.makedirs('data', exist_ok=True)

print('Welcome to the Contact Book!')
menu = ['Add Contact', 'View Contacts', 'Search Contact', 'Update Contact', 'Delete Contact', 'Exit']

for ind, opt in enumerate(menu):
    print(f'{ind+1}. {opt}')
print()        
main()