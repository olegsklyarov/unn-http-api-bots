# State-based filtering
Паттерн "Dispatcher - Handler" — хэндлеры запускаются только при нужном апдейте.
State-based filtering — хэндлеры запускаются только в нужном состоянии пользователя.
## Database Layer
- **Users table**: `id`, `telegram_id` (UNIQUE), `created_at`, `state`, `data`
- **User management functions**: `ensure_user_exists()`,  `get_user()`, `update_user_state()`
## Handlers
- + хэндлер `EnsureUserExists` (создать пользователя если еще нет, не останавливающий ❗)
- dispatch:
	- получает telegram_id из апдейта
	- достает из БД текущий state
	- передает state при вызове хэндлера
- Каждый хэндлер принимает на вход `state: dict` (функции `can_handle()`, `handle()`)

<Реализация>

# 🍕 Pizza Shop Telegram Bot
## Phase 1: Database Schema & User State (15 minutes)

### Step 1: User State Management
**Teaching Points:**
- **State Machine Design**: `WAIT_FOR_PIZZA_NAME` → `WAIT_FOR_PIZZA_SIZE` → `WAIT_FOR_DRINKS` → `WAIT_FOR_ORDER_APPROVE` → `ORDER_FINISHED`
- **JSON Data Storage**: Store complex order data as JSON strings in database
- **User Lifecycle**: Ensure user exists, track state, accumulate order data
- **Data Persistence**: Order builds up incrementally across multiple interactions
## Phase 2: Start Handler - Order Initialization (10 minutes)

### Step 2: Message Start Handler
**Teaching Points:**
- **Order Reset**: Clear previous order data when starting new order
- **State Initialization**: Set initial state to begin order flow
- **UI Cleanup**: Remove old keyboards for clean user experience
- **Inline Keyboard Creation**: Present choices as clickable buttons
- **Command Handling**: Process `/start` command to begin order process
## Phase 3: Pizza Selection Handler (15 minutes)

### Step 3: Pizza Selection Handler
**Teaching Points:**
- **State-based Filtering**: Only respond when user is in correct state
- **Callback Data Processing**: Extract pizza name from `pizza_margherita` format
- **Data Storage**: Save user selection to database
- **State Progression**: Move user to next step in order flow
- **UI Flow Management**: Delete previous message, show next step
- **User Feedback**: Answer callback query to acknowledge button press
## Phase 4: Pizza Size Handler (15 minutes)

### Step 4: Pizza Size Handler
**Teaching Points:**
- **Data Aggregation**: Preserve existing order data, add new selection
- **JSON Parsing**: Handle existing order data with error handling
- **Mapping Strategy**: Convert callback codes to user-friendly names
- **Data Accumulation**: Build complete order object step by step
- **State Transitions**: Progress user through order flow
- **Error Handling**: Graceful fallback for malformed data

## Phase 5: Drinks Handler (15 minutes)

### Step 5: Pizza Drinks Handler
**Teaching Points:**
- **Order Completion**: Finalize order with all selections
- **Data Summarization**: Display complete order for user review
- **Markdown Formatting**: Use rich text formatting for better UX
- **Approval Workflow**: Present options to confirm or restart
- **State Management**: Move to approval state
- **User Experience**: Clear, formatted order summary
## Phase 6: Order Approval Handler (15 minutes)

### Step 6: Order Approval Handler
**Teaching Points:**
- **Dual Path Handling**: Process both approval and restart actions
- **Order Completion**: Final confirmation with order details
- **Data Reset**: Clear all data for fresh start
- **Method Decomposition**: Separate approval and restart logic
- **Final State**: Mark order as completed
- **User Journey**: Complete order lifecycle from start to finish

## Phase 7: Handler Registration (5 minutes)

### Step 7: Register All Handlers
**Teaching Points:**
- **Handler Ordering**: Critical for proper flow execution
- **Dependency Management**: Ensure user exists before processing orders
- **Complete Flow**: All handlers work together for seamless experience
- **Modular Design**: Each handler has single responsibility
## Key Learning Outcomes

### **Business Logic Concepts:**
1. **State Machine**: User progresses through defined states
2. **Data Accumulation**: Order builds up step by step
3. **User Experience**: Clean UI with message deletion
4. **Order Management**: Complete order lifecycle

### **Technical Patterns:**
1. **State-based Filtering**: Handlers only respond in specific states
2. **Data Persistence**: JSON storage for complex order data
3. **UI Flow Management**: Delete previous, show next
4. **Error Handling**: JSON parsing with fallbacks

### **Pizza Shop Features:**
- ✅ Pizza type selection
- ✅ Size selection
- ✅ Drink selection
- ✅ Order summary
- ✅ Order approval/restart
- ✅ Order confirmation