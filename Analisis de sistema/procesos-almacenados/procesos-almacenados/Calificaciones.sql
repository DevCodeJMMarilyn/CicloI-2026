USE manzanares;

DROP PROCEDURE IF EXISTS GenerarCalificaciones;

DELIMITER //

CREATE PROCEDURE GenerarCalificaciones()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE t_id INT;
    
    DECLARE cur CURSOR FOR SELECT ticket_id FROM ticket_solutions;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO t_id;
        IF done THEN
            LEAVE read_loop;
        END IF;

        INSERT INTO qualifications (
            score,       -- Nota del 1 al 5
            comment,     -- Comentario aleatorio
            ticket_id,   -- ID del ticket calificado
            deleted_at, 
            created_at, 
            updated_at
        ) VALUES (
            FLOOR(3 + (RAND() * 3)), -- Genera notas entre 3 y 5 
            ELT(FLOOR(1 + (RAND() * 5)), 
                'Excelente servicio', 'Muy rápido', 'Solucionado correctamente', 
                'Buena atención', 'Satisfecho con el soporte'),
            t_id,
            NULL,
            NOW(),
            NOW()
        );
    END LOOP;

    CLOSE cur;
END //

DELIMITER ;

-- EJECUCIÓN
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE qualifications;
CALL GenerarCalificaciones();
SET FOREIGN_KEY_CHECKS = 1;