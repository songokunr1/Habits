# Habits


users
- id (primary key)
- email
- password_hash

projects
- id (primary key)
- name
- description

user_info
- id (primary key)
- user_id (foreign key to users.id)
- first_name
- last_name
- phone_number

addresses
- id (primary key)
- user_id (foreign key to users.id)
- line_1
- line_2
- city
- state
- country

user_projects
- user_id (foreign key to users.id)
- project_id (foreign key to projects.id)
- role (foreign key to roles.id)

project_roles
- id (primary key)
- project_id (foreign key to projects.id)
- user_id (foreign key to users.id)
- role_name 



roles: Admin, free-user, premium-user, 
