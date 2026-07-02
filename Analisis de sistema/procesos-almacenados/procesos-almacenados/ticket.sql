USE manzanares;

DROP PROCEDURE IF EXISTS GenerarTickets;

DELIMITER //

CREATE PROCEDURE GenerarTickets()
BEGIN
    DECLARE i INT DEFAULT 1;
    DECLARE current_user_id INT;
    DECLARE current_email VARCHAR(255);
    DECLARE assigned_tech_id INT;
    DECLARE random_status INT;
    
    WHILE i <= 1000 DO
        SET current_user_id = IF(RAND() > 0.5, 6, 7);
        SELECT email INTO current_email FROM users WHERE id = current_user_id;
        
        SET assigned_tech_id = IF(RAND() > 0.5, 4, 5);
        SET random_status = FLOOR(2 + (RAND() * 5)); 

        INSERT INTO tickets (
            code, creation_date, email, subject, message, 
            expiration_date, closing_date, requesting_user, assigned_user, 
            help_topic_id, priority_id, sla_plan_id, 
            department_id, status_id, created_at, updated_at
        ) VALUES (
            CONCAT('TK-', 2026, LPAD(i, 4, '0')),
            DATE_ADD('2026-04-01', INTERVAL (RAND() * 28) DAY),
            current_email,
            ELT(FLOOR(1 + (RAND() * 3)), 'Falla de Hardware', 'Error de Software', 'Problema de Red'),
            'Simulación de flujo de trabajo con estados variados.',
            DATE_ADD(NOW(), INTERVAL 7 DAY),
            DATE_ADD(                                          
			DATE_ADD('2026-04-02', INTERVAL (RAND() * 28) DAY),
			INTERVAL (1 + FLOOR(RAND() * 8)) HOUR         
		),
            current_user_id,
            assigned_tech_id,
            FLOOR(1 + (RAND() * 3)), 
            FLOOR(2 + (RAND() * 3)), 
            FLOOR(1 + (RAND() * 2)), 
            FLOOR(1 + (RAND() * 3)), 
            random_status, 
            NOW(),
            NOW()
        );
        SET i = i + 1;
    END WHILE;
END //

DELIMITER ;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE tickets;
CALL GenerarTickets();
SET FOREIGN_KEY_CHECKS = 1;