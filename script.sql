DROP TABLE IF EXISTS Posts;

CREATE TABLE Posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,       -- Unique identifier for each entry
    name TEXT NOT NULL,                         -- Name of the person/entity
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, -- Date and time of creation
                                                -- Stored as TEXT in ISO8601 format (YYYY-MM-DD HH:MM:SS)
    description TEXT,                           -- A textual description
    location TEXT                               -- Location as a string (e.g., "New York, USA", "Room 101")
);

INSERT INTO Posts (name, created_at, description, location) VALUES
(
    'Nguyễn Văn An',
    '2024-03-10 23:55:00',
    'Trận lũ quét kinh hoàng tại Sa Pa, cuốn trôi nhiều nhà cửa và gây thiệt hại nặng nề về hoa màu. Mọi người đang khẩn trương sơ tán.',
    'Sa Pa, Lào Cai'
),
(
    'Trần Thị Bích',
    '2024-03-11 12:30:15',
    'Hạn hán kéo dài ở Đồng Tháp khiến kênh rạch khô cạn, đồng ruộng nứt nẻ. Nông dân đối mặt với nguy cơ mất trắng mùa màng.',
    'Đồng Tháp'
),
(
    'Lê Văn Cường',
    '2024-03-09 08:15:45',
    'Sạt lở đất nghiêm trọng xảy ra tại Mộc Châu sau những ngày mưa lớn, chia cắt nhiều tuyến đường và cô lập các bản làng.',
    'Tân Lập, Mộc Châu, Sơn La'
);

