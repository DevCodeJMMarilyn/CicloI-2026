USE manzanares;

DROP PROCEDURE IF EXISTS GenerarSoluciones;

DELIMITER //

CREATE PROCEDURE GenerarSoluciones()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE t_id INT;
    DECLARE t_subject VARCHAR(255);
    DECLARE random_tech INT;
    
    -- Cursor para encontrar tickets que necesitan solución 
    DECLARE cur CURSOR FOR SELECT id, subject FROM tickets WHERE id > 0;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO t_id, t_subject;
        IF done THEN
            LEAVE read_loop;
        END IF;

        -- Elegimos un técnico al azar 
        SET random_tech = FLOOR(1 + (RAND() * 4));

        INSERT INTO ticket_solutions (
            ticket_id, 
            user_id, 
            message, 
            date, 
            solution_type_id, 
            created_at, 
            updated_at
        ) VALUES (
            t_id,
            random_tech,
            CONCAT('Solución aplicada al caso de: ', t_subject, '. Se verificó el correcto funcionamiento y se cerró el incidente.'),
            DATE_ADD('2026-04-01', INTERVAL (RAND() * 28) DAY),
            FLOOR(1 + (RAND() * 4)), -- Tipos de solución del 1 al 4
            NOW(),
            NOW()
        );
    END LOOP;

    CLOSE cur;
END //

DELIMITER ;

-- EJECUCIÓN
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE ticket_solutions;
CALL GenerarSoluciones();
SET FOREIGN_KEY_CHECKS = 1;