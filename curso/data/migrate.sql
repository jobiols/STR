/* pasar info del tilde presente al estado */
update curso_assistance
set state = 'present'
where present = True;

/* eliminar basura */
delete from curso_lecture
where date_start is null;

update curso_curso
set email_registration_id = 40
where email_registration_id is null

delete from curso_assistance
where lecture_id is null