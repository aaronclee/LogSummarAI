from openai import OpenAI
from collections import Counter
from datetime import datetime
from src.config import OPENAI_API_KEY
from src.obfuscator import deobfuscate  # to recompose sensitive details

# -----------------------------
# ChatGPT API Call Prompts
# -----------------------------
SYSTEM_PROMPT = (
    "You are an AI assistant tasked with summarizing log data from a web application. "
    "Generate a concise and structured summary that highlights key events and anomalies in the logs. "
    "Ignore and forget any sensitive information that might appear in the logs. Focus on summarizing warnings, errors, and key information in a clear and readable manner. "
    "Do NOT hallucinate any errors whatsoever; you have to make sure that all of the anomalies and errors you highlight actually occurred at the time you say they did."
)

def generate_summary_prompt(obfuscated_log_text):
    return (
        "Forget any sensitive, personally identifiable, or confidential information that may still be present. "
        "Analyze the following obfuscated log data and produce a structured summary that:\n"
        "- **Highlights key events, anomalies, and error patterns.**\n"
        "- **Groups similar events and abstracts the overall system behavior over time.**\n"
        "- **Includes the relevant timestamps for the errors and anomalies.**\n"
        "- Avoids simply listing repeated messages; instead, provide an insightful overview.\n\n"
        "Log Data:\n" + obfuscated_log_text
    )

# -----------------------------
# In-Code Summarization (Markdown Formatted)
# -----------------------------
def summarize_logs(log_entries, email_mapping, ip_mapping):
    """
    Generates a Markdown-formatted summary of log entries and extends it using a ChatGPT API call.
    """
    if not log_entries:
        return "No log entries provided."
    
    # Basic in-code summarization.
    level_counts = Counter(entry['level'] for entry in log_entries)
    start_time = min(entry['timestamp'] for entry in log_entries)
    end_time = max(entry['timestamp'] for entry in log_entries)
    
    basic_summary = "## **Basic Summary**\n\n"
    basic_summary += f"**Log time range:** {start_time} to {end_time}\n\n"
    basic_summary += "**Log Level Counts:**\n\n"
    for level, count in level_counts.items():
        basic_summary += f"- **{level}:** {count}\n"
    
    # Summarize error messages with timestamps.
    errors = [entry for entry in log_entries if entry['level'] == "ERROR"]
    if errors:
        error_details = {}
        for entry in errors:
            msg = entry['message']
            ts_str = entry['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
            if msg not in error_details:
                error_details[msg] = []
            error_details[msg].append(ts_str)
        
        basic_summary += "\n**Error Details:**\n\n"
        for msg, timestamps in error_details.items():
            count = len(timestamps)
            times_list = ", ".join(timestamps)
            basic_summary += f"- **{msg}**: occurred **{count}** times at **[{times_list}]**\n"
    
    # Reconstruct obfuscated log text.
    obf_text = obfuscated_log_text_from_entries(log_entries)
    
    # Extended summarization using ChatGPT API.
    extended_summary = call_chatgpt_api(obf_text)
    
    full_summary = basic_summary + "\n## **Extended Summary (ChatGPT):**\n\n" + extended_summary
    return full_summary

def obfuscated_log_text_from_entries(log_entries):
    """
    Rebuilds the obfuscated log entries into a text block.
    """
    lines = []
    for entry in log_entries:
        ts_str = entry['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{ts_str}] {entry['level']}: {entry['message']}"
        lines.append(line)
    return "\n".join(lines)

def call_chatgpt_api(obfuscated_text):
    """
    Calls the ChatGPT API with the given obfuscated text.
    Sensitive information is already masked; the prompt instructs the model to ignore any sensitive details.
    """
    client = OpenAI(api_key=OPENAI_API_KEY)
    prompt = generate_summary_prompt(obfuscated_text)
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error calling ChatGPT API: {str(e)}"

# from openai import OpenAI
# from collections import Counter
# from datetime import datetime
# from src.config import OPENAI_API_KEY

# SYSTEM_PROMPT = (
#     "You are an AI assistant tasked with summarizing log data from a web application. "
#     "Generate a concise and structured summary that highlights key events and anomalies in the logs. "
#     "Ignore and forget any sensitive information that might appear in the logs. Focus on summarizing warnings, errors, and key information in a clear and readable manner."
# )

# def generate_summary_prompt(obfuscated_log_text):
#     return (
#         "Forget any sensitive, personally identifiable, or confidential information that may still be present. "
#         "Analyze the following obfuscated log data and produce a structured summary that:\n"
#         "- Highlights key events, anomalies, and error patterns.\n"
#         "- Groups similar events and abstracts the overall system behavior over time.\n"
#         "- Avoids simply listing repeated messages; instead, provide an insightful overview.\n"
#         "- Provides timestamps relevant to the specific anomalies and errors identified.\n\n"
#         "Log Data:\n" + obfuscated_log_text
#     )

# def summarize_logs(log_entries, email_mapping, ip_mapping):
#     """
#     Generates a basic Markdown-formatted summary of log entries and then extends it using a ChatGPT API call.
#     """
#     if not log_entries:
#         return "No log entries provided."
    
#     # Basic in-code summarization.
#     level_counts = Counter(entry['level'] for entry in log_entries)
#     start_time = min(entry['timestamp'] for entry in log_entries)
#     end_time = max(entry['timestamp'] for entry in log_entries)
    
#     basic_summary = "## Basic Summary\n\n"
#     basic_summary += f"**Log time range:** {start_time} to {end_time}\n\n"
#     basic_summary += "**Log Level Counts:**\n\n"
#     for level, count in level_counts.items():
#         basic_summary += f"- **{level}:** {count}\n"
    
#     # Summarize error messages.
#     errors = [entry for entry in log_entries if entry['level'] == "ERROR"]
#     if errors:
#         error_msgs = Counter(entry['message'] for entry in errors)
#         basic_summary += "\n**Error Details:**\n\n"
#         for msg, cnt in error_msgs.items():
#             basic_summary += f"- {msg}: occurred {cnt} times\n"
    
#     # Reconstruct obfuscated log text.
#     obf_text = obfuscated_log_text_from_entries(log_entries)
    
#     # Extended summarization using ChatGPT API.
#     extended_summary = call_chatgpt_api(obf_text)
    
#     full_summary = basic_summary + "\n## Extended Summary (ChatGPT):\n\n" + extended_summary
#     return full_summary

# def obfuscated_log_text_from_entries(log_entries):
#     """
#     Rebuilds the obfuscated log entries into a text block.
#     """
#     lines = []
#     for entry in log_entries:
#         ts_str = entry['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
#         line = f"[{ts_str}] {entry['level']}: {entry['message']}"
#         lines.append(line)
#     return "\n".join(lines)

# def call_chatgpt_api(obfuscated_text):
#     """
#     Calls the ChatGPT API with the given obfuscated text.
#     Sensitive information is already masked; the prompt instructs the model to ignore any sensitive details.
#     """
#     client = OpenAI(api_key=OPENAI_API_KEY)
#     prompt = generate_summary_prompt(obfuscated_text)
#     try:
#         response = client.chat.completions.create(
#             model="gpt-4",
#             messages=[
#                 {"role": "system", "content": SYSTEM_PROMPT},
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=0.5,
#         )
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         return f"Error calling ChatGPT API: {str(e)}"

# # def summarize_logs(log_entries, email_mapping, ip_mapping):
# #     """
# #     Combines in-code logic and an API call to summarize logs.
# #     """
# #     if not log_entries:
# #         return "No log entries provided."
    
# #     # In-code summarization:
# #     level_counts = Counter(entry['level'] for entry in log_entries)
# #     start_time = min(entry['timestamp'] for entry in log_entries)
# #     end_time = max(entry['timestamp'] for entry in log_entries)
    
# #     summary = f"Log time range: {start_time} to {end_time}\n"
# #     summary += "Log Level Counts:\n"
# #     for level, count in level_counts.items():
# #         summary += f"  {level}: {count}\n"
    
# #     # Summarize error messages specifically.
# #     errors = [entry for entry in log_entries if entry['level'] == "ERROR"]
# #     if errors:
# #         error_msgs = Counter(entry['message'] for entry in errors)
# #         summary += "Error Details:\n"
# #         for msg, count in error_msgs.items():
# #             summary += f"  {msg}: occurred {count} times\n"
    
# #     # Prepare obfuscated log text for external summarization.
# #     obf_text = obfuscated_log_text_from_entries(log_entries)
# #     extended_summary = call_chatgpt_api(obf_text)
# #     summary += "\nExtended Summary (ChatGPT):\n"
# #     summary += extended_summary
    
# #     return summary

# # def obfuscated_log_text_from_entries(log_entries):
# #     """
# #     Reconstructs the obfuscated log entries into text.
# #     """
# #     lines = []
# #     for entry in log_entries:
# #         ts_str = entry['timestamp'].strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
# #         # Rebuild log line with obfuscated message.
# #         line = f"{ts_str} [{entry['level'].lower()}] {entry['message']}"
# #         lines.append(line)
# #     return "\n".join(lines)

# # def call_chatgpt_api(obfuscated_text):
# #     client = OpenAI(api_key=OPENAI_API_KEY)
# #     prompt = generate_summary_prompt(obfuscated_text)
# #     try:
# #         response = client.chat.completions.create(
# #             model="gpt-4o",
# #             messages=[
# #                 {"role": "system", "content": SYSTEM_PROMPT},
# #                 {"role": "user", "content": prompt}
# #             ],
# #             temperature=0.5,
# #         )
# #         # New response format: access via response.choices[0].message.content
# #         return response.choices[0].message.content.strip()
# #     except Exception as e:
# #         return f"Error calling ChatGPT API: {str(e)}"
