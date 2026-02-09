# 💬 Realtime Chat Platform (Django + WebSockets)

A full-stack **realtime messaging platform** built with **Django, Django Channels, WebSockets, and Redis**.
This project demonstrates how to design and implement a **distributed, event-driven system** inside a traditional web framework.

> ⚡ Not just a chat demo — this project showcases realtime architecture, connection lifecycle management, presence tracking, and scalable message broadcasting.

---

## 🚀 Features

### 🔹 Realtime Messaging

- Instant message delivery using **WebSockets**
- No page reloads, no polling
- Message validation and persistence before broadcast

### 🔹 Presence System

- Live online user tracking per room
- Updates triggered by connection lifecycle (connect/disconnect)
- Realtime presence synchronization across all clients

### 🔹 Private Conversations

- One-to-one private chat rooms
- Membership-based access control
- Dynamic room creation

### 🔹 Distributed Architecture

- Redis-backed channel layer
- Supports multiple ASGI workers
- Designed for horizontal scaling

### 🔹 Conversation Navigation

- Global chat dropdown
- Private chat index
- Conversation-aware UI

---

## 🧠 System Architecture Overview

This application is built as a **distributed realtime system**, not just a Django app.

```

Browser
│
│ WebSocket
▼
Django Channels Consumer
│
├── Validation Layer (Django Forms)
├── Persistence Layer (PostgreSQL)
└── Broadcast Layer (Redis Channel Layer)
│
▼
Other Connected Clients

```

The system operates across **two communication planes**:

| Layer         | Purpose                                       |
| ------------- | --------------------------------------------- |
| **HTTP**      | Page rendering, authentication, room creation |
| **WebSocket** | Live events (messages, presence, updates)     |

---

## 🧩 Tech Stack

| Technology          | Purpose                                           |
| ------------------- | ------------------------------------------------- |
| **Django**          | Core web framework                                |
| **Django Channels** | WebSocket support & event routing                 |
| **ASGI**            | Enables long-lived connections and async handling |
| **Redis**           | Distributed channel layer backend                 |
| **PostgreSQL**      | Persistent storage for users, rooms, messages     |
| **Alpine.js**       | Reactive frontend updates                         |
| **Tailwind CSS**    | UI styling                                        |

---

## ⚙️ Key Concepts Demonstrated

### 🔌 WebSocket Lifecycle

Each client connection is managed by a **Consumer**, which handles:

- `connect()` → join room, update presence
- `receive()` → validate, save, broadcast messages
- `disconnect()` → cleanup presence

### 📨 Event-Driven Messaging

The WebSocket connection carries multiple event types:

```json
{ "event": "message", "message": {...} }
{ "event": "online_count", "online_count": 4 }
```

A custom event protocol enables multiplexed realtime communication over a single socket.

### 📡 Channel Layer (Redis)

The channel layer acts as a **message bus**:

- Routes events between consumers
- Synchronizes state across multiple server workers
- Enables horizontal scaling

### 👥 Presence Modeling

Presence is modeled as **shared state**, not just events:

- Stored in the database
- Updated on connection lifecycle
- Broadcast to all clients in the room

### 🔒 Realtime Security

WebSocket consumers enforce:

- Authentication
- Room-level authorization
- Private room membership validation

---

## 🗂️ Project Structure (Key Parts)

```
a_rtchat/
│
├── consumers.py      # WebSocket connection controllers
├── models.py         # Chat rooms, messages, presence
├── views.py          # HTTP layer for room bootstrap
├── queries.py        # Chat relationship data access
├── serializers.py    # Transport formatting
├── context_processors.py  # Global chat data injection
│
templates/
├── chat.html         # Chat interface
└── partials/         # Chat dropdown & UI components
```

---

## 🧪 Running the Project

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Start Redis

```bash
redis-server
```

### 3️⃣ Run Migrations

```bash
python manage.py migrate
```

### 4️⃣ Start ASGI Server

```bash
daphne a_core.asgi:application
```

---

## 🏗️ What This Project Proves

This project demonstrates practical experience with:

- Realtime system design
- Distributed event-driven architecture
- WebSocket lifecycle management
- Scalable Django deployment patterns
- Separation of concerns across layers
- Designing communication protocols

---

## 📌 Why This Matters

Modern applications like Slack, Discord, and collaborative tools rely on the same architectural patterns demonstrated here:

- Persistent connections
- Message buses
- Presence tracking
- Event multiplexing
- Distributed coordination

This project shows the ability to build these systems from the ground up.

---

## 👨‍💻 Author

Built as part of advanced exploration into **realtime web architecture** and **scalable backend systems**.

---
