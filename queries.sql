-- 1. Отримую всі завдання користувача з id 1
SELECT * FROM tasks
WHERE user_id = 1;

-- 2. Отримую всі завдання зі статусом new
SELECT * FROM tasks
WHERE status_id = (
    SELECT id FROM status
    WHERE name = 'new'
);

-- 3. Змінюю статус завдання з id 1 на in progress
UPDATE tasks
SET status_id = (
    SELECT id FROM status
    WHERE name = 'in progress'
)
WHERE id = 1;

-- 4. Знаходжу користувачів, які не мають завдань
SELECT * FROM users
WHERE id NOT IN (
    SELECT user_id FROM tasks
    WHERE user_id IS NOT NULL
);

-- 5. Додаю нове завдання для користувача з id 1
INSERT INTO tasks (title, description, status_id, user_id)
VALUES (
    'New task',
    'Task description',
    (SELECT id FROM status WHERE name = 'new'),
    1
);

-- 6. Отримую всі незавершені завдання
SELECT * FROM tasks
WHERE status_id != (
    SELECT id FROM status
    WHERE name = 'completed'
);

-- 7. Видаляю завдання з id 2
DELETE FROM tasks
WHERE id = 2;

-- 8. Знаходжу користувачів за частиною електронної пошти
SELECT * FROM users
WHERE email LIKE '%example.com%';

-- 9. Змінюю ім'я користувача з id 1
UPDATE users
SET fullname = 'New User Name'
WHERE id = 1;

-- 10. Підраховую кількість завдань для кожного статусу
SELECT status_id, COUNT(*) AS task_count
FROM tasks
GROUP BY status_id;

-- 11. Знаходжу завдання користувачів із поштою домену example.com
SELECT tasks.*
FROM tasks
JOIN users ON tasks.user_id = users.id
WHERE users.email LIKE '%@example.com';

-- 12. Отримую завдання без опису
SELECT * FROM tasks
WHERE description IS NULL OR description = '';

-- 13. Знаходжу користувачів та їхні завдання зі статусом in progress
SELECT users.fullname, tasks.title
FROM users
INNER JOIN tasks ON users.id = tasks.user_id
INNER JOIN status ON tasks.status_id = status.id
WHERE status.name = 'in progress';

-- 14. Підраховую кількість завдань кожного користувача
SELECT users.id, users.fullname, COUNT(tasks.id) AS task_count
FROM users
LEFT JOIN tasks ON users.id = tasks.user_id
GROUP BY users.id, users.fullname;