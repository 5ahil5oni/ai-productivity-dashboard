import pandas as pd
import numpy as np

# --- Configuration ---
NUM_ROWS = 1000

# --- Lists of Choices ---
ROLES_DATA = {
    'Developer': {
        'department': 'Tech',
        'tasks': ['Coding Help', 'Bug Fixing', 'Code Review', 'Documentation'],
        'tools_weights': [0.35, 0.05, 0.35, 0.2, 0.05] # Weights for [ChatGPT, Notion AI, Copilot, Gemini, Other]
    },
    'Data Analyst': {
        'department': 'Tech',
        'tasks': ['Data Analysis', 'Report Writing', 'Query Generation', 'Visualization'],
        'tools_weights': [0.3, 0.15, 0.1, 0.4, 0.05]
    },
    'Designer': {
        'department': 'Marketing',
        'tasks': ['Ideation', 'Image Generation', 'Asset Creation', 'Copywriting'],
        'tools_weights': [0.2, 0.3, 0.1, 0.35, 0.05]
    },
    'Manager': {
        'department': 'Management',
        'tasks': ['Email Drafting', 'Report Writing', 'Scheduling', 'Strategy'],
        'tools_weights': [0.3, 0.2, 0.1, 0.3, 0.1]
    },
    'Marketing Specialist': {
        'department': 'Marketing',
        'tasks': ['Copywriting', 'Ideation', 'Email Drafting', 'Market Research'],
        'tools_weights': [0.3, 0.25, 0.05, 0.35, 0.05]
    },
    'HR Specialist': {
        'department': 'HR',
        'tasks': ['Email Drafting', 'Job Description Writing', 'Report Writing', 'Policy Q&A'],
        'tools_weights': [0.4, 0.2, 0.05, 0.3, 0.05]
    },
    'Financial Analyst': {
        'department': 'Finance',
        'tasks': ['Report Writing', 'Data Analysis', 'Forecasting', 'Email Drafting'],
        'tools_weights': [0.4, 0.1, 0.1, 0.3, 0.1]
    }
}

ALL_ROLES = list(ROLES_DATA.keys())
ALL_TOOLS = ['ChatGPT', 'Notion AI', 'Copilot', 'Gemini', 'Other']
EXPERIENCE_LEVELS = ['Junior', 'Mid', 'Senior']
USAGE_FREQUENCIES = ['Daily', 'Weekly', 'Occasional']
COUNTRIES = ['USA', 'India', 'UK', 'Germany', 'Canada', 'Australia', 'Japan']
REMOTE_STATUSES = ['Remote', 'Office', 'Hybrid']

# --- Helper Functions ---
def get_tool(role, task):
    """Get a weighted tool choice based on role."""
    # Clone the list to prevent mutating the original dictionary
    weights = ROLES_DATA[role]['tools_weights'].copy()
    
    # If task is coding-related, boost Copilot
    if task in ['Coding Help', 'Bug Fixing', 'Code Review']:
        weights[2] = weights[2] * 2.0 # Boost Copilot
    # If task is ideation/writing, boost Gemini/Notion
    if task in ['Ideation', 'Copywriting', 'Strategy']:
        weights[1] = weights[1] * 1.5 # Boost Notion AI
        weights[3] = weights[3] * 1.5 # Boost Gemini
    
    # Normalize weights so they sum to 1
    weights = np.array(weights)
    weights /= weights.sum()
    
    return np.random.choice(ALL_TOOLS, p=weights)

def get_remote_status(department):
    """Get weighted remote status based on department."""
    if department in ['Tech', 'Marketing']:
        p = [0.5, 0.1, 0.4] # High Remote/Hybrid
    elif department in ['Finance', 'HR']:
        p = [0.1, 0.5, 0.4] # High Office/Hybrid
    else:
        p = [0.3, 0.3, 0.4] # Balanced
    return np.random.choice(REMOTE_STATUSES, p=p)

# --- Main Data Generation ---
print(f"Generating {NUM_ROWS} rows of synthetic data...")

data = []
for i in range(1, NUM_ROWS + 1):
    # --- 1. Generate Base Attributes ---
    user_id = f'U{str(i).zfill(4)}'
    user_role = np.random.choice(ALL_ROLES, p=[0.25, 0.15, 0.1, 0.1, 0.15, 0.1, 0.15]) # Weighted roles
    department = ROLES_DATA[user_role]['department']
    experience_level = np.random.choice(EXPERIENCE_LEVELS, p=[0.3, 0.5, 0.2]) # More Mid-level
    task_type = np.random.choice(ROLES_DATA[user_role]['tasks'])
    ai_tool_used = get_tool(user_role, task_type)
    usage_frequency = np.random.choice(USAGE_FREQUENCIES, p=[0.6, 0.3, 0.1]) # Mostly Daily
    country = np.random.choice(COUNTRIES, p=[0.4, 0.2, 0.1, 0.1, 0.05, 0.05, 0.1])
    remote_status = get_remote_status(department)
    
    # --- 2. Generate Correlated Numerical Data ---
    # Add department-based variance noise to hours worked
    base_hours = 42
    if department in ['Tech', 'Marketing']:
        scale = 5 # Higher variance
    elif department in ['Finance', 'HR']:
        scale = 3 # Lower variance
    else:
        scale = 4 # Average variance
        
    hours_worked_per_week = np.random.normal(loc=base_hours, scale=scale)
    hours_worked_per_week = np.clip(hours_worked_per_week, 30, 60) # Clip to realistic bounds
    
    # --- 3. Generate Target Variable (time_saved_per_week) ---
    # This is the most important part for modeling
    base_time_saved = np.random.normal(loc=5, scale=2)
    
    # Add bonus based on frequency
    if usage_frequency == 'Daily':
        freq_bonus = np.random.normal(3, 1)
    elif usage_frequency == 'Weekly':
        freq_bonus = np.random.normal(1, 0.5)
    else:
        freq_bonus = np.random.normal(0, 0.5)
        
    # Add bonus based on experience
    if experience_level == 'Senior':
        exp_bonus = np.random.normal(2, 0.5)
    elif experience_level == 'Mid':
        exp_bonus = np.random.normal(1, 0.5)
    else: # Junior
        exp_bonus = np.random.normal(0.5, 0.5)
        
    # Add bonus based on tool (e.g., Copilot is great for coding time saving)
    if ai_tool_used == 'Copilot' and task_type in ['Coding Help', 'Bug Fixing']:
        tool_bonus = np.random.normal(3, 1)
    elif ai_tool_used in ['Gemini', 'ChatGPT'] and task_type in ['Report Writing', 'Copywriting']:
        tool_bonus = np.random.normal(1, 0.5)
    else:
        tool_bonus = np.random.normal(0, 0.5)
        
    time_saved_per_week = base_time_saved + freq_bonus + exp_bonus + tool_bonus
    time_saved_per_week = np.clip(time_saved_per_week, 0.5, 25) # Clip to 30 min to 25 hours
    
    # --- 4. Generate Other Dependant Metrics ---
    
    # Performance is highly correlated with time saved
    performance_improvement_pct = (time_saved_per_week * 2.5) + np.random.normal(0, 3)
    performance_improvement_pct = np.clip(performance_improvement_pct, 1, 75)
    
    # Satisfaction is correlated with time saved and tool
    satisfaction_base = (time_saved_per_week / 20) * 10 # Scale time saved to 0-10
    
    tool_satisfaction_bonus = 0
    if ai_tool_used == 'Gemini': tool_satisfaction_bonus = np.random.normal(1, 0.5)
    if ai_tool_used == 'Notion AI': tool_satisfaction_bonus = np.random.normal(0.5, 0.5)
    if ai_tool_used == 'Other': tool_satisfaction_bonus = np.random.normal(-1, 0.5)

    satisfaction_score = satisfaction_base + tool_satisfaction_bonus + np.random.normal(0, 0.5)
    satisfaction_score = np.clip(satisfaction_score, 1, 10)

    # --- 5. Append Row ---
    data.append({
        'user_id': user_id,
        'user_role': user_role,
        'department': department,
        'experience_level': experience_level,
        'task_type': task_type,
        'AI_tool_used': ai_tool_used,
        'hours_worked_per_week': round(hours_worked_per_week, 1),
        'time_saved_per_week': round(time_saved_per_week, 1),
        'satisfaction_score': int(round(satisfaction_score, 0)),
        'performance_improvement_pct': round(performance_improvement_pct, 1), # Renamed column
        'usage_frequency': usage_frequency,
        'country': country,
        'remote_status': remote_status
    })

# --- 6. Create DataFrame and Save ---
df = pd.DataFrame(data)

# Add a numeric index column for ML
df['employee_index'] = np.arange(1, NUM_ROWS + 1)

# Reorder columns to match request
column_order = [
    'employee_index', 'user_id', 'user_role', 'department', 'experience_level', 'task_type',
    'AI_tool_used', 'hours_worked_per_week', 'time_saved_per_week',
    'satisfaction_score', 'performance_improvement_pct', 'usage_frequency', # Updated name
    'country', 'remote_status'
]
df = df[column_order]

# --- 7. Save to CSV ---
output_filename = 'synthetic_ai_professional_data.csv'
df.to_csv(output_filename, index=False)

print(f"\nSuccessfully generated {NUM_ROWS} rows and saved to '{output_filename}'.")
print("\n--- DataFrame Head ---")
print(df.head())
print("\n--- DataFrame Info ---")
df.info()