CREATE TABLE ratings (
    restaurant_id TEXT,
    user_id TEXT,
    rating INTEGER,
    PRIMARY KEY (restaurant_id, user_id)
);

INSERT INTO ratings (user_id, restaurant_id, rating) 
VALUES 
    ('U1', 'R1', 1),
    ('U1', 'R3', 3),
    ('U1', 'R6', 5),
    ('U1', 'R9', 5),
    ('U1', 'R11', 4),
    -- USER 2 
    ('U2', 'R3', 5),
    ('U2', 'R4', 4),
    ('U2', 'R7', 4),
    ('U2', 'R10', 2),
    ('U2', 'R11', 1),
    ('U2', 'R12', 3),
    -- USER 3
    ('U3', 'R1', 2),
    ('U3', 'R2', 4),
    ('U3', 'R4', 1),
    ('U3', 'R5', 2),
    ('U3', 'R7', 3),
    ('U3', 'R9', 4),
    ('U3', 'R10', 3),
    ('U3', 'R11', 5),
    -- USER 4
    ('U4', 'R2', 2),
    ('U4', 'R3', 4),
    ('U4', 'R5', 5),
    ('U4', 'R8', 4),
    ('U4', 'R11', 2),
    -- USER 5
    ('U5', 'R3', 4),
    ('U5', 'R4', 3),
    ('U5', 'R5', 4),
    ('U5', 'R6', 2),
    ('U5', 'R11', 2),
    ('U5', 'R12', 5),
    -- USER 6 
    ('U6', 'R1', 1),
    ('U6', 'R3', 3),
    ('U6', 'R5', 3),
    ('U6', 'R8', 2),
    ('U6', 'R11', 4);
