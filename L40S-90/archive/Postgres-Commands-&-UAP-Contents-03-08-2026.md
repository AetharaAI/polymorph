## UAP Postgres Instance Triad-VM   

docker container: uap-postgres
Main_DB: uap
superuser: uap_core


Common postgres commands: 
** Example using litellm_admin as Role and litellm_db as DB
CREATE ROLE litellm_admin WITH LOGIN PASSWORD 'litellm_admin_2026_infra';

ALTER ROLE litellm_admin WITH LOGIN PASSWORD 'your_new_password_here';

CREATE DATABASE litellm_db OWNER litellm_admin;

ALTER DATABASE litellm_db OWNER TO litellm_admin;

GRANT ALL PRIVILEGES ON DATABASE litellm_db TO litellm_admin;

to Connect to db:
\c litellm_db
to list db's:
\l
to list roles:
\du
to list tables:
\dt

* Database List:

                                                           List of databases
        Name        |  Owner   | Encoding | Locale Provider |  Collate   |   Ctype    | ICU Locale | ICU Rules |   Access privileges   
--------------------+----------+----------+-----------------+------------+------------+------------+-----------+-----------------------
 aetherai           | uap_core | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           | =Tc/uap_core         +
                    |          |          |                 |            |            |            |           | uap_core=CTc/uap_core
 aetherauth         | uap_core | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           | =Tc/uap_core         +
                    |          |          |                 |            |            |            |           | uap_core=CTc/uap_core
 aetherfleet        | uap_core | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           | 
 aetheros           | uap_core | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           | 
 aetherpro_research | uap_core | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           | 
 agentforge         | uap_core | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           | =Tc/uap_core         +
                    |          |          |                 |            |            |            |           | uap_core=CTc/uap_core
 blackboxaudio      | uap_core | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           | =Tc/uap_core         +
                    |          |          |                 |            |            |            |           | uap_core=CTc/uap_core
 buildengine        | uap_core | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           | 
 cie_db             | uap_core | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           | 
 fluxmini           | uap_core | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           | =Tc/uap_core         +
                    |          |          |                 |            |            |            |           | uap_core=CTc/uap_core
 litellm            | uap_core | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           | 
 msah               | uap_core | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           | 
 percy_control      | percy    | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           | =Tc/percy            +
                    |          |          |                 |            |            |            |           | percy=CTc/percy
 persiai            | uap_core | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           | =Tc/uap_core         +
                    |          |          |                 |            |            |            |           | uap_core=CTc/uap_core
 postgres           | uap_core | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           | 
 sentinel           | uap_core | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           | =Tc/uap_core         +
                    |          |          |                 |            |            |            |           | uap_core=CTc/uap_core
 template0          | uap_core | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           | =c/uap_core          +
                    |          |          |                 |            |            |            |           | uap_core=CTc/uap_core
 template1          | uap_core | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           | =c/uap_core          +
                    |          |          |                 |            |            |            |           | uap_core=CTc/uap_core
 uap_core           | uap_core | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           | 
(19 rows)

~


