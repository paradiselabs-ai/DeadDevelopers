from fasthtml.common import *
from fasthtml.svg import Svg, ft_svg as tag
from pathlib import Path
import json
from typing import Dict, List
from app import rt

# Create dashboard-specific headers
dashboard_css = Link(rel='stylesheet', href='/css/dashboard.css', type='text/css')

# Add inline styles for scrollbar to ensure they apply
scrollbar_styles = Style("""
    /* Ensure scrollbar styles apply globally */
    html, body {
        scrollbar-width: thin; /* For Firefox */
        scrollbar-color: #333 #1e1e1e; /* For Firefox */
    }

    ::-webkit-scrollbar {
        width: 8px !important;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #1e1e1e !important;
    }

    ::-webkit-scrollbar-thumb {
        background: #333;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #444 !important;
    }
""")

# Helper components for icons
def MenuIcon():
    return Svg(
        tag("line", x1="3", y1="12", x2="21", y2="12"),
        tag("line", x1="3", y1="6", x2="21", y2="6"),
        tag("line", x1="3", y1="18", x2="21", y2="18"),
        viewBox="0 0 24 24", width="20", height="20", stroke="currentColor",
        strokeWidth="2", fill="none"
    )

def HomeIcon():
    return Svg(
        tag("path", d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"),
        tag("polyline", points="9 22 9 12 15 12 15 22"),
        viewBox="0 0 24 24", width="20", height="20", stroke="currentColor",
        strokeWidth="2", fill="none"
    )

def ProjectsIcon():
    return Svg(
        tag("path", d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"),
        tag("polyline", points="14 2 14 8 20 8"),
        tag("line", x1="16", y1="13", x2="8", y2="13"),
        tag("line", x1="16", y1="17", x2="8", y2="17"),
        tag("polyline", points="10 9 9 9 8 9"),
        viewBox="0 0 24 24", width="20", height="20", stroke="currentColor",
        strokeWidth="2", fill="none"
    )

def AnalyticsIcon():
    return Svg(
        tag("line", x1="18", y1="20", x2="18", y2="10"),
        tag("line", x1="12", y1="20", x2="12", y2="4"),
        tag("line", x1="6", y1="20", x2="6", y2="14"),
        viewBox="0 0 24 24", width="20", height="20", stroke="currentColor",
        strokeWidth="2", fill="none"
    )

def TeamIcon():
    return Svg(
        tag("path", d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"),
        tag("circle", cx="9", cy="7", r="4"),
        tag("path", d="M23 21v-2a4 4 0 0 0-3-3.87"),
        tag("path", d="M16 3.13a4 4 0 0 1 0 7.75"),
        viewBox="0 0 24 24", width="20", height="20", stroke="currentColor",
        strokeWidth="2", fill="none"
    )

def DocsIcon():
    return Svg(
        tag("path", d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"),
        tag("path", d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"),
        viewBox="0 0 24 24", width="20", height="20", stroke="currentColor",
        strokeWidth="2", fill="none"
    )

def SettingsIcon():
    return Svg(
        tag("circle", cx="12", cy="12", r="3"),
        tag("path", d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"),
        viewBox="0 0 24 24", width="20", height="20", stroke="currentColor",
        strokeWidth="2", fill="none"
    )

def SearchIcon():
    return Svg(
        tag("circle", cx="11", cy="11", r="8"),
        tag("line", x1="21", y1="21", x2="16.65", y2="16.65"),
        viewBox="0 0 24 24", width="18", height="18", stroke="currentColor",
        strokeWidth="2", fill="none"
    )

def NotificationIcon():
    return Svg(
        tag("path", d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"),
        tag("path", d="M13.73 21a2 2 0 0 1-3.46 0"),
        viewBox="0 0 24 24", width="20", height="20", stroke="currentColor",
        strokeWidth="2", fill="none"
    )

def TeamNotificationIcon():
    return Svg(
        tag("path", d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"),
        tag("circle", cx="9", cy="7", r="4"),
        tag("path", d="M23 21v-2a4 4 0 0 0-3-3.87"),
        tag("path", d="M16 3.13a4 4 0 0 1 0 7.75"),
        viewBox="0 0 24 24", width="14", height="14", stroke="currentColor",
        strokeWidth="2", fill="currentColor"
    )

def StarIconNotification(width=14, height=14):
    return Svg(
        tag("polygon", points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"),
        viewBox="0 0 24 24", width=width, height=height, stroke="currentColor",
        strokeWidth="2", fill="currentColor"
    )

def MessageIcon():
    return Svg(
        tag("path", d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"),
        viewBox="0 0 24 24", width="14", height="14", stroke="currentColor",
        strokeWidth="2", fill="currentColor"
    )

def MessageSquareIcon(width=20, height=20):
    return Svg(
        tag("path", d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"),
        viewBox="0 0 24 24", width=width, height=height, stroke="currentColor",
        strokeWidth="2", fill="none"
    )

def SendIcon():
    return Svg(
        tag("line", x1="22", y1="2", x2="11", y2="13"),
        tag("polygon", points="22 2 15 22 11 13 2 9 22 2"),
        viewBox="0 0 24 24", width="18", height="18", stroke="currentColor",
        strokeWidth="2", fill="none", strokeLinecap="round", strokeLinejoin="round"
    )

def UsersIcon(width=16, height=16):
    return Svg(
        tag("path", d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"),
        tag("circle", cx="9", cy="7", r="4"),
        tag("path", d="M23 21v-2a4 4 0 0 0-3-3.87"),
        tag("path", d="M16 3.13a4 4 0 0 1 0 7.75"),
        viewBox="0 0 24 24", width=width, height=height, stroke="currentColor",
        strokeWidth="2", fill="none"
    )

def XIcon():
    return Svg(
        tag("line", x1="18", y1="6", x2="6", y2="18"),
        tag("line", x1="6", y1="6", x2="18", y2="18"),
        viewBox="0 0 24 24", width="20", height="20", stroke="currentColor",
        strokeWidth="2", fill="none"
    )

def StarIcon(width=15, height=15):
    return Svg(
        tag("polygon", points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"),
        viewBox="0 0 24 24", width=width, height=height, stroke="#00FF00",
        strokeWidth="2", fill="none"
    )

def EditProfileIcon():
    return Svg(
        tag("path", d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"),
        tag("path", d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"),
        viewBox="0 0 24 24", width="16", height="16", stroke="currentColor",
        strokeWidth="2", fill="none"
    )

def BillingIcon():
    return Svg(
        tag("rect", x="1", y="4", width="22", height="16", rx="2", ry="2"),
        tag("line", x1="1", y1="10", x2="23", y2="10"),
        viewBox="0 0 24 24", width="16", height="16", stroke="currentColor",
        strokeWidth="2", fill="none"
    )

def SecurityIcon():
    return Svg(
        tag("rect", x="3", y="11", width="18", height="11", rx="2", ry="2"),
        tag("path", d="M7 11V7a5 5 0 0 1 10 0v4"),
        viewBox="0 0 24 24", width="16", height="16", stroke="currentColor",
        strokeWidth="2", fill="none"
    )

def SignOutIcon():
    return Svg(
        tag("path", d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"),
        tag("polyline", points="16 17 21 12 16 7"),
        tag("line", x1="21", y1="12", x2="9", y2="12"),
        viewBox="0 0 24 24", width="16", height="16", stroke="currentColor",
        strokeWidth="2", fill="none"
    )

def PlusIcon():
    return Svg(
        tag("line", x1="12", y1="5", x2="12", y2="19"),
        tag("line", x1="5", y1="12", x2="19", y2="12"),
        viewBox="0 0 24 24", width="16", height="16", stroke="currentColor",
        strokeWidth="2", fill="none"
    )

def ArrowIcon():
    return Svg(
        tag("line", x1="7", y1="17", x2="17", y2="7"),
        tag("polyline", points="7 7 17 7 17 17"),
        viewBox="0 0 24 24", width="18", height="18", stroke="currentColor",
        strokeWidth="2", fill="none"
    )

def DotsIcon():
    return Svg(
        tag("circle", cx="12", cy="12", r="1"),
        tag("circle", cx="19", cy="12", r="1"),
        tag("circle", cx="5", cy="12", r="1"),
        viewBox="0 0 24 24", width="20", height="20", stroke="currentColor",
        strokeWidth="2", fill="currentColor"
    )

def CalendarIcon():
    return Svg(
        tag("rect", x="3", y="4", width="18", height="18", rx="2", ry="2"),
        tag("line", x1="16", y1="2", x2="16", y2="6"),
        tag("line", x1="8", y1="2", x2="8", y2="6"),
        tag("line", x1="3", y1="10", x2="21", y2="10"),
        viewBox="0 0 24 24", width="12", height="12", stroke="currentColor",
        strokeWidth="2", fill="none"
    )

# Global Chat CSS
global_chat_css = Link(rel='stylesheet', href='/css/global-chat.css', type='text/css')

# We don't need a separate function for global chat JS since it's already handled in get_toggle_js

# Mock data for chat messages and users
def get_mock_messages():
    """Return mock chat messages for the global chat"""
    return [
        {
            "id": "msg1",
            "user": {"name": "Alex Rivera", "avatar": "\img\code-avatar.svg", "online": True},
            "message": "Has anyone tried the new AI model training pipeline?",
            "timestamp": "12:30"
        },
        {
            "id": "msg2",
            "user": {"name": "Jamie Liu", "avatar": "\img\code-avatar.svg", "online": True},
            "message": "Yes, it's much faster than the previous version. I was able to train my model in half the time.",
            "timestamp": "12:35"
        },
        {
            "id": "msg3",
            "user": {"name": "Taylor Swift", "avatar": "\img\code-avatar.svg", "online": False},
            "message": "I'm still having issues with the Discord API rate limiting. Any workarounds?",
            "timestamp": "12:45"
        },
        {
            "id": "msg4",
            "user": {"name": "Morgan Reed", "avatar": "\img\code-avatar.svg", "online": True},
            "message": "Try implementing a queue system with exponential backoff. I can share my code if you need it.",
            "timestamp": "12:50"
        },
        {
            "id": "msg5",
            "user": {"name": "DeadDev_42", "avatar": "\img\code-avatar.svg", "online": True},
            "message": "That would be great! Can you post it in the DeadBot repo as a gist?",
            "timestamp": "12:55"
        }
    ]

def get_mock_users():
    """Return mock online users for the global chat"""
    return [
        {"id": "1", "name": "Alex Rivera", "avatar": "\img\code-avatar.svg", "status": "online"},
        {"id": "2", "name": "Jamie Liu", "avatar": "\img\code-avatar.svg", "status": "online"},
        {"id": "3", "name": "Taylor Swift", "avatar": "\img\code-avatar.svg", "status": "away"},
        {"id": "4", "name": "Morgan Reed", "avatar": "\img\code-avatar.svg", "status": "busy"},
        {"id": "5", "name": "Jordan Davis", "avatar": "\img\code-avatar.svg", "status": "online"},
        {"id": "6", "name": "Casey Kim", "avatar": "\img\code-avatar.svg", "status": "online"},
        {"id": "7", "name": "Riley Johnson", "avatar": "\img\code-avatar.svg", "status": "away"}
    ]

def GlobalChat(is_open=False):
    """
    Global Chat component that provides a chat sidebar with tabs for messages and online users.

    Args:
        is_open: Boolean indicating if the chat sidebar should be open by default

    Returns:
        A Div containing the global chat component with the global_chat_css
    """
    # Get mock data
    messages = get_mock_messages()
    online_users = get_mock_users()
    online_count = len([user for user in online_users if user["status"] == "online"])

    # Create message elements
    message_elements = [
        Div(
            Div(
                Img(src=msg["user"]["avatar"] or "/placeholder.svg", alt=f"{msg['user']['name']}'s avatar", cls="message-avatar"),
                # Removed status indicator circle
                cls="message-avatar-container"
            ),
            Div(
                Div(
                    Span(msg["user"]["name"], cls="message-sender"),
                    Span("online", cls="user-status-text online") if msg["user"]["online"] else Span("offline", cls="user-status-text offline"),
                    Span(msg["timestamp"], cls="message-time"),
                    cls="message-header"
                ),
                P(msg["message"], cls="message-text"),
                cls="message-content"
            ),
            cls="chat-message",
            id=f"message-{msg['id']}"
        ) for msg in messages
    ]

    # Create user elements
    user_elements = [
        Div(
            Div(
                Img(src=user["avatar"] or "/placeholder.svg", alt=f"{user['name']}'s avatar", cls="user-avatar"),
                Div(cls=f"status-indicator {user['status']}"),
                Div(user["status"].capitalize(), cls="status-tooltip"),
                cls="user-avatar-container"
            ),
            Div(
                Div(
                    Span(user["name"], cls="user-name"),
                    Span(user["status"], cls=f"user-status-text {user['status']}"),
                    cls="user-info-header"
                ),
                P("Active now" if user["status"] == "online" else "", cls="user-last-seen"),
                cls="user-info"
            ),
            cls="user-item",
            id=f"user-{user['id']}"
        ) for user in online_users
    ]

    # Chat component structure
    return Div(global_chat_css,
        # Chat overlay with transition
        Div(
            cls=f"chat-overlay {'opacity-100 pointer-events-auto' if is_open else 'hidden'}",
            id="chat-overlay",
            style=f"opacity: {1 if is_open else 0}; transition: opacity 0.3s ease-in-out, visibility 0.3s ease-in-out;"
        ),

        # Chat sidebar with transition styles
        Div(
            # Header
            Div(
                Div(
                    H2("Global Chat", cls="chat-title"),
                    Div(f"{online_count} online", cls="online-badge"),
                    cls="chat-header-title"
                ),
                Button(
                    XIcon(),
                    cls="chat-close-button",
                    id="close-chat-button"
                ),
                cls="chat-header"
            ),

            # Tabs
            Div(
                Button(
                    Div(
                        MessageSquareIcon(width=16, height=16),
                        Span("Chat"),
                        Div(cls="unread-indicator", id="chat-unread-indicator"),
                        cls="chat-tab-content"
                    ),
                    cls="chat-tab active",
                    id="chat-tab-button",
                    onclick="switchChatTab('chat')"
                ),
                Button(
                    Div(
                        UsersIcon(width=16, height=16),
                        Span("Users"),
                        Div(cls="unread-indicator", id="users-unread-indicator"),
                        cls="chat-tab-content"
                    ),
                    cls="chat-tab",
                    id="users-tab-button",
                    onclick="switchChatTab('users')"
                ),
                cls="chat-tabs"
            ),

            # Add JavaScript for tab switching and chat input functionality
            Script("""
            // Function to handle unread indicators
            function handleUnreadIndicators() {
                const chatUnreadIndicator = document.getElementById('chat-unread-indicator');
                const usersUnreadIndicator = document.getElementById('users-unread-indicator');
                let currentTab = 'chat'; // Default active tab

                // Function to show unread indicator for a specific tab
                function showUnreadIndicator(tab) {
                    if (tab === 'chat' && currentTab !== 'chat') {
                        chatUnreadIndicator.classList.add('active');
                    } else if (tab === 'users' && currentTab !== 'users') {
                        usersUnreadIndicator.classList.add('active');
                    }
                }

                // Simulate new messages and user status changes
                setInterval(() => {
                    // 15% chance of new message when not on chat tab
                    if (Math.random() < 0.15 && currentTab !== 'chat') {
                        showUnreadIndicator('chat');
                    }

                    // 10% chance of user status change when not on users tab
                    if (Math.random() < 0.1 && currentTab !== 'users') {
                        showUnreadIndicator('users');
                    }
                }, 15000); // Check every 15 seconds

                // Update current tab reference
                window.updateCurrentTab = function(tab) {
                    currentTab = tab;

                    // Clear the unread indicator for the active tab
                    if (tab === 'chat') {
                        chatUnreadIndicator.classList.remove('active');
                    } else if (tab === 'users') {
                        usersUnreadIndicator.classList.remove('active');
                    }
                };
            }

            // Function to switch between chat tabs with simple animations
            function switchChatTab(tabName) {
                // Get elements
                const chatContent = document.getElementById('chat-content');
                const usersContent = document.getElementById('users-content');
                const chatTabButton = document.getElementById('chat-tab-button');
                const usersTabButton = document.getElementById('users-tab-button');
                const headerTitle = document.querySelector('#chat-sidebar h2');
                const tabsContainer = document.querySelector('.chat-tabs');

                // Prevent rapid tab switching by checking if animation is in progress
                if (document.querySelector('.tab-switching-in-progress')) {
                    return;
                }

                // Update current tab for unread indicators
                if (window.updateCurrentTab) {
                    window.updateCurrentTab(tabName);
                }

                // Mark that tab switching is in progress
                document.body.classList.add('tab-switching-in-progress');

                if (tabName === 'chat') {
                    // Update tab indicator
                    tabsContainer.classList.remove('users-active');

                    // Update active tab styling
                    chatTabButton.classList.add('active');
                    usersTabButton.classList.remove('active');

                    // Update header
                    if (headerTitle) {
                        headerTitle.textContent = "Global Chat";
                    }

                    // Hide users content, show chat content
                    usersContent.classList.remove('slide-in');
                    usersContent.classList.add('slide-out');

                    // Show chat content
                    chatContent.style.display = 'flex';
                    chatContent.classList.remove('slide-out');
                    chatContent.classList.add('slide-in');

                    // Focus on the chat input
                    setTimeout(() => {
                        const chatInput = document.getElementById('chat-message-input');
                        if (chatInput) chatInput.focus();

                        // Hide users content after transition
                        usersContent.style.display = 'none';

                        // Remove the in-progress flag
                        document.body.classList.remove('tab-switching-in-progress');
                    }, 250);
                } else {
                    // Update tab indicator
                    tabsContainer.classList.add('users-active');

                    // Update active tab styling
                    chatTabButton.classList.remove('active');
                    usersTabButton.classList.add('active');

                    // Update header
                    if (headerTitle) {
                        headerTitle.textContent = "Online Users";
                    }

                    // Hide chat content, show users content
                    chatContent.classList.remove('slide-in');
                    chatContent.classList.add('slide-out');

                    // Show users content
                    usersContent.style.display = 'block';
                    usersContent.classList.remove('slide-out');
                    usersContent.classList.add('slide-in');

                    // Hide chat content after transition
                    setTimeout(() => {
                        chatContent.style.display = 'none';

                        // Remove the in-progress flag
                        document.body.classList.remove('tab-switching-in-progress');
                    }, 250);
                }
            }

            // Store the send icon SVG for reuse
            const sendIconSvg = '<svg viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>';

            // Function to reset button to its default state
            function resetButtonToDefaultState(button) {
                // Remove any inline styles that might interfere with CSS
                button.removeAttribute('style');
                button.className = 'chat-send-button';
            }

            // Function to create a ripple effect on tab buttons
            function createRipple(event) {
                const button = event.currentTarget;

                // Remove any existing ripples
                const ripples = button.getElementsByClassName('ripple');
                for (let i = 0; i < ripples.length; i++) {
                    button.removeChild(ripples[i]);
                }

                // Create ripple element
                const circle = document.createElement('span');
                const diameter = Math.max(button.clientWidth, button.clientHeight);
                const radius = diameter / 2;

                // Position the ripple based on click location
                const rect = button.getBoundingClientRect();
                circle.style.width = circle.style.height = `${diameter}px`;
                circle.style.left = `${event.clientX - rect.left - radius}px`;
                circle.style.top = `${event.clientY - rect.top - radius}px`;
                circle.classList.add('ripple');

                // Add the ripple to the button
                button.appendChild(circle);

                // Remove the ripple after animation completes
                setTimeout(() => {
                    if (circle && circle.parentNode === button) {
                        button.removeChild(circle);
                    }
                }, 600);
            }

            // Add ripple effect to tab buttons
            document.addEventListener('DOMContentLoaded', function() {
                const tabButtons = document.querySelectorAll('.chat-tab');
                tabButtons.forEach(button => {
                    button.addEventListener('click', createRipple);
                });

                // Initialize status tooltips
                initializeStatusTooltips();
            });

            // Function to initialize status tooltips
            function initializeStatusTooltips() {
                // Get all status indicators
                const statusIndicators = document.querySelectorAll('.status-indicator');

                // Add mouseover event to show tooltip with status information
                statusIndicators.forEach(indicator => {
                    indicator.addEventListener('mouseover', function() {
                        // Find the tooltip
                        const tooltip = this.nextElementSibling;
                        if (tooltip && tooltip.classList.contains('status-tooltip')) {
                            // Update tooltip text based on status
                            if (this.classList.contains('online')) {
                                tooltip.textContent = 'Online';
                            } else if (this.classList.contains('away')) {
                                tooltip.textContent = 'Away';
                            } else if (this.classList.contains('busy')) {
                                tooltip.textContent = 'Do Not Disturb';
                            } else if (this.classList.contains('offline')) {
                                tooltip.textContent = 'Offline';
                            }
                        }
                    });
                });
            }

            // Track message sending metrics
            let messagesSent = 0;
            let lastMessageSentTime = 0;
            let lastActivityTime = Date.now();
            let showSuccessThreshold = 1000; // Show success for messages that take longer than 1 second
            let sessionTimeout = 10 * 60 * 1000; // Reset counter after 10 minutes of inactivity

            // Function to send a chat message using fetch API
            function sendChatMessage() {
                const chatInput = document.getElementById('chat-message-input');
                const sendButton = document.getElementById('send-message-button');
                const chatMessages = document.getElementById('chat-messages');
                const indicator = document.getElementById('chat-sending-indicator');

                // Check if we need to reset the session counter due to inactivity
                const now = Date.now();
                if (now - lastActivityTime > sessionTimeout) {
                    messagesSent = 0; // Reset the counter if user was inactive
                }
                lastActivityTime = now;

                // Get the message text
                const messageText = chatInput.value.trim();
                if (!messageText) return;

                // Record the start time for this message
                const sendStartTime = Date.now();
                lastMessageSentTime = sendStartTime;

                // Show the sending indicator and update button state
                if (indicator) {
                    // Clear any existing classes or styles
                    indicator.className = 'chat-sending-indicator htmx-request';
                    indicator.innerHTML = '<span class="chat-sending-text"><span style="display:inline-block;vertical-align:middle;">Sending...</span></span>';
                    indicator.style.display = 'flex';
                    indicator.style.opacity = '1';
                }

                // Disable the button and change its appearance while sending
                if (sendButton) {
                    // First reset to default state to clear any inline styles
                    resetButtonToDefaultState(sendButton);

                    // Then update to sending state
                    sendButton.disabled = true;
                    sendButton.className = 'chat-send-button sending';
                    sendButton.innerHTML = '<svg viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" stroke-width="2" fill="none"><circle cx="12" cy="12" r="10" opacity="0.3"></circle><path d="M12 2a10 10 0 0 1 10 10" stroke-linecap="round"><animateTransform attributeName="transform" type="rotate" from="0 12 12" to="360 12 12" dur="1s" repeatCount="indefinite"/></path></svg>';
                }

                // Create form data
                const formData = new FormData();
                formData.append('message', messageText);

                // Send the request
                fetch('/chat_send', {
                    method: 'POST',
                    body: formData
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Server responded with status: ${response.status}`);
                    }
                    return response.text();
                })
                .then(html => {
                    // Check if the response contains an error message
                    if (html.includes('error-message')) {
                        // Extract the error message
                        const tempDiv = document.createElement('div');
                        tempDiv.innerHTML = html;
                        const errorMsg = tempDiv.textContent || 'Unknown error';
                        console.error('Server error:', errorMsg);

                        // Add an error message to the chat
                        if (chatMessages) {
                            const errorElement = document.createElement('div');
                            errorElement.className = 'chat-message system-message';
                            errorElement.innerHTML = `<div class="message-content"><p class="message-text error-text">Failed to send message: ${errorMsg}</p></div>`;
                            chatMessages.appendChild(errorElement);
                            chatMessages.scrollTop = chatMessages.scrollHeight;
                        }
                    } else if (html.trim()) {
                        // Add the new message to the chat
                        if (chatMessages) {
                            chatMessages.insertAdjacentHTML('beforeend', html);
                            chatMessages.scrollTop = chatMessages.scrollHeight;
                        }

                        // Clear the input
                        chatInput.value = '';
                    }

                    // Calculate how long the message took to send
                    const sendDuration = Date.now() - lastMessageSentTime;
                    messagesSent++;

                    // Hide the sending indicator with a slight delay for better UX
                    setTimeout(() => {
                        if (indicator) {
                            indicator.classList.remove('htmx-request');

                            // Only show success message in specific cases:
                            // 1. First 2 messages sent by the user
                            // 2. Messages that took longer than the threshold to send
                            // 3. Every 10th message as a reassurance
                            const shouldShowSuccess =
                                messagesSent <= 2 ||
                                sendDuration > showSuccessThreshold ||
                                messagesSent % 10 === 0;

                            if (shouldShowSuccess) {
                                // Show a brief success message with animation
                                indicator.className = 'chat-sending-indicator visible';
                                indicator.innerHTML = '<span class="chat-sending-text success"><span style="display:inline-block;vertical-align:middle;">Sent</span></span>';

                                // Add a subtle animation
                                indicator.style.transform = 'translateY(-0.5rem)';

                                // Hide the success message after 1.5 seconds with a smooth fade
                                setTimeout(() => {
                                    indicator.style.opacity = '0';
                                    indicator.style.transform = 'translateY(-1rem)';
                                    setTimeout(() => {
                                        indicator.style.display = 'none';
                                        indicator.innerHTML = '<span class="chat-sending-text"><span style="display:inline-block;vertical-align:middle;">Sending...</span></span>';
                                    }, 300);
                                }, 1500);
                            } else {
                                // Just reset the indicator without showing success
                                indicator.style.opacity = '0';
                                indicator.style.transform = 'translateY(-1rem)';
                                setTimeout(() => {
                                    indicator.style.display = 'none';
                                    indicator.innerHTML = '<span class="chat-sending-text"><span style="display:inline-block;vertical-align:middle;">Sending...</span></span>';
                                }, 300);
                            }
                        }
                    }, 300);

                    // Restore the send button with a subtle animation
                    if (sendButton) {
                        // Reset button to default state
                        resetButtonToDefaultState(sendButton);

                        // Update state
                        sendButton.disabled = !chatInput.value.trim();
                        sendButton.innerHTML = sendIconSvg;

                        // Add a subtle pop animation when the button is restored
                        if (!sendButton.disabled) {
                            sendButton.animate([
                                { transform: 'scale(0.92)' },
                                { transform: 'scale(1.05)' },
                                { transform: 'scale(1)' }
                            ], {
                                duration: 350,
                                easing: 'cubic-bezier(0.175, 0.885, 0.32, 1.275)'
                            });
                        }
                    }

                    // Focus the input again
                    chatInput.focus();
                })
                .catch(error => {
                    console.error('Error sending message:', error);

                    // Add an error message to the chat
                    if (chatMessages) {
                        const errorElement = document.createElement('div');
                        errorElement.className = 'chat-message system-message';
                        errorElement.innerHTML = `<div class="message-content"><p class="message-text error-text">Failed to send message: ${error.message}</p></div>`;
                        chatMessages.appendChild(errorElement);
                        chatMessages.scrollTop = chatMessages.scrollHeight;
                    }

                    // Update the sending indicator to show error
                    if (indicator) {
                        indicator.className = 'chat-sending-indicator visible';
                        indicator.innerHTML = '<span class="chat-sending-text error"><span style="display:inline-block;vertical-align:middle;">Failed</span></span>';
                        indicator.style.transform = 'translateY(-0.5rem)';

                        // Hide the error message after 3 seconds with a smooth fade
                        setTimeout(() => {
                            indicator.style.opacity = '0';
                            indicator.style.transform = 'translateY(-1rem)';
                            setTimeout(() => {
                                indicator.style.display = 'none';
                                indicator.innerHTML = '<span class="chat-sending-text"><span style="display:inline-block;vertical-align:middle;">Sending...</span></span>';
                            }, 300);
                        }, 3000);
                    }

                    // Restore the send button with error state indication
                    if (sendButton) {
                        // Reset button to default state
                        resetButtonToDefaultState(sendButton);

                        // Update state
                        sendButton.disabled = !chatInput.value.trim();
                        sendButton.innerHTML = sendIconSvg;

                        // Add a subtle shake animation to indicate error
                        sendButton.animate([
                            { transform: 'translateX(-4px)' },
                            { transform: 'translateX(4px)' },
                            { transform: 'translateX(-3px)' },
                            { transform: 'translateX(3px)' },
                            { transform: 'translateX(0)' }
                        ], {
                            duration: 400,
                            easing: 'ease-out'
                        });
                    }
                });
            }

            // Simulate typing indicator
            function simulateTypingIndicator() {
                const typingIndicator = document.getElementById('typing-indicator');
                const typingText = document.querySelector('.typing-indicator-text');
                const users = ['Alex', 'Jamie', 'Morgan', 'Taylor', 'Jordan'];

                // Show typing indicator randomly
                setInterval(() => {
                    // 20% chance to show typing indicator if not already active
                    if (Math.random() < 0.2 && !typingIndicator.classList.contains('active')) {
                        // Select random user
                        const user = users[Math.floor(Math.random() * users.length)];
                        typingText.textContent = `${user} is typing...`;

                        // Show indicator
                        typingIndicator.classList.add('active');

                        // Scroll to bottom if user is near bottom already
                        const chatMessages = document.getElementById('chat-messages');
                        if (chatMessages.scrollHeight - chatMessages.scrollTop - chatMessages.clientHeight < 100) {
                            chatMessages.scrollTop = chatMessages.scrollHeight;
                        }

                        // Hide after random time (2-5 seconds)
                        setTimeout(() => {
                            typingIndicator.classList.remove('active');
                        }, 2000 + Math.random() * 3000);
                    }
                }, 10000); // Check every 10 seconds
            }

            // Initialize chat input functionality when the DOM is loaded
            document.addEventListener('DOMContentLoaded', function() {
                const chatInput = document.getElementById('chat-message-input');
                const sendButton = document.getElementById('send-message-button');
                const chatMessages = document.getElementById('chat-messages');
                const chatContent = document.getElementById('chat-content');
                const usersContent = document.getElementById('users-content');

                // Initialize typing indicator simulation
                simulateTypingIndicator();

                // Initialize unread indicators
                handleUnreadIndicators();

                // Ensure initial tab state is correct
                if (chatContent) {
                    chatContent.classList.add('slide-in');
                    chatContent.classList.remove('slide-out');
                }

                if (usersContent) {
                    usersContent.classList.add('slide-out');
                    usersContent.classList.remove('slide-in');
                }

                // Enable/disable send button based on input
                if (chatInput && sendButton) {
                    // Reset button to default state and disable it
                    resetButtonToDefaultState(sendButton);
                    sendButton.disabled = true;

                    // Add focus/blur classes instead of inline styles
                    chatInput.addEventListener('focus', function() {
                        this.classList.add('chat-input-focused');
                    });

                    chatInput.addEventListener('blur', function() {
                        this.classList.remove('chat-input-focused');
                    });

                    chatInput.addEventListener('input', function() {
                        sendButton.disabled = !this.value.trim();

                        // Add subtle animation when enabling the button
                        if (!sendButton.disabled && sendButton.dataset.wasDisabled === 'true') {
                            sendButton.animate([
                                { transform: 'scale(0.95)', opacity: 0.7 },
                                { transform: 'scale(1.05)', opacity: 1 },
                                { transform: 'scale(1)', opacity: 1 }
                            ], {
                                duration: 250,
                                easing: 'cubic-bezier(0.175, 0.885, 0.32, 1.275)'
                            });
                        }

                        // Track disabled state
                        sendButton.dataset.wasDisabled = sendButton.disabled.toString();
                    });

                    // Enable keyboard shortcut (Enter to send)
                    chatInput.addEventListener('keydown', function(e) {
                        if (e.key === 'Enter' && !e.shiftKey && !sendButton.disabled) {
                            e.preventDefault();
                            sendChatMessage();
                        }
                    });
                }

                // Initial scroll to bottom of messages
                if (chatMessages) {
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                }
            });
            """),

            # Content
            Div(
                # Messages tab
                Div(
                    # Messages container with scrolling
                    Div(
                        *message_elements,
                        # Add typing indicator
                        Div(
                            Div(
                                Span("Someone is typing", cls="typing-indicator-text"),
                                Div(
                                    Div(cls="typing-indicator-dot"),
                                    Div(cls="typing-indicator-dot"),
                                    Div(cls="typing-indicator-dot"),
                                    cls="typing-indicator-dots"
                                ),
                                cls="typing-indicator-content"
                            ),
                            cls="typing-indicator",
                            id="typing-indicator"
                        ),
                        id="chat-messages",
                        cls="chat-messages"
                    ),
                    # Input container (fixed at bottom)
                    Div(
                        Div(
                            Input(
                                type="text",
                                placeholder="Type a message...",
                                cls="chat-input",
                                id="chat-message-input",
                                name="message",
                                autocomplete="off"
                            ),
                            Button(
                                SendIcon(),
                                type="button", # Changed to button instead of submit
                                cls="chat-send-button",
                                id="send-message-button",
                                disabled=True,
                                title="Send message",
                                onclick="sendChatMessage()"
                            ),
                            cls="chat-input-form",
                            id="chat-form"
                        ),
                        Div(
                            Span(
                                Span("Sending message...", style="display:inline-block;vertical-align:middle;"),
                                cls="chat-sending-text"
                            ),
                            cls="chat-sending-indicator",
                            id="chat-sending-indicator"
                        ),
                        cls="chat-input-container"
                    ),
                    id="chat-content",
                    cls="chat-content slide-in",
                    style="display: flex;"
                ),

                # Users tab with scrolling
                Div(
                    Div(
                        *user_elements,
                        cls="users-list-content"
                    ),
                    id="users-content",
                    cls="users-list slide-out",
                    style="display: none;"
                ),

                cls="chat-content-wrapper"
            ),

            cls=f"chat-sidebar {'visible' if is_open else 'hidden'}",
            id="chat-sidebar",
            style=f"transform: translateX({'0' if is_open else '100%'}); opacity: {1 if is_open else 0}; transition: transform 0.3s ease-in-out, opacity 0.3s ease-in-out;"
        ),
        cls="global-chat-container",
        hx_ext="global-chat"  # Custom extension for additional behavior if needed
    )

# JavaScript for toggling sidebar and dropdowns
def get_toggle_js():
    return """
    document.addEventListener('DOMContentLoaded', function() {
        const sidebarToggle = document.getElementById('sidebar-toggle');
        const menuButton = document.getElementById('menu-button');
        const sidebar = document.getElementById('sidebar');
        const overlay = document.querySelector('.sidebar-overlay');
        const notificationButton = document.getElementById('notification-button');
        const notificationDropdown = document.querySelector('.notification-dropdown');
        const userMenuButton = document.getElementById('user-menu-button');
        const userDropdown = document.querySelector('.user-dropdown');

        // Chat elements
        const chatButton = document.getElementById('chat-button');
        const chatSidebar = document.getElementById('chat-sidebar');
        const chatOverlay = document.getElementById('chat-overlay');
        const closeChatButton = document.getElementById('close-chat-button');
        const chatTabButton = document.getElementById('chat-tab-button');
        const usersTabButton = document.getElementById('users-tab-button');
        const chatContent = document.getElementById('chat-content');
        const chatForm = document.getElementById('chat-form');
        const chatMessageInput = document.getElementById('chat-message-input');
        const chatMessages = document.getElementById('chat-messages');

        // Check if mobile
        const checkMobile = () => {
            const isMobile = window.innerWidth < 768;
            if (isMobile) {
                sidebar.classList.remove('desktop-open', 'desktop-closed');
                sidebar.classList.add('mobile-closed');
            } else {
                sidebar.classList.remove('mobile-open', 'mobile-closed');
                sidebar.classList.add('desktop-closed');
            }
        };

        checkMobile();
        window.addEventListener('resize', checkMobile);

        // Toggle sidebar
        if (sidebarToggle) {
            sidebarToggle.addEventListener('click', function() {
                if (sidebar.classList.contains('mobile-closed')) {
                    sidebar.classList.remove('mobile-closed');
                    sidebar.classList.add('mobile-open');
                    overlay.classList.add('active');
                } else if (sidebar.classList.contains('mobile-open')) {
                    sidebar.classList.remove('mobile-open');
                    sidebar.classList.add('mobile-closed');
                    overlay.classList.remove('active');
                } else if (sidebar.classList.contains('desktop-closed')) {
                    sidebar.classList.remove('desktop-closed');
                    sidebar.classList.add('desktop-open');
                    overlay.classList.add('active');
                } else {
                    sidebar.classList.remove('desktop-open');
                    sidebar.classList.add('desktop-closed');
                    overlay.classList.remove('active');
                }

                // Close dropdowns when sidebar is toggled
                if (notificationDropdown) notificationDropdown.style.display = 'none';
                if (userDropdown) userDropdown.style.display = 'none';
                // Close chat sidebar when main sidebar is toggled
                if (chatSidebar) chatSidebar.style.transform = 'translateX(100%)';
                if (chatOverlay) chatOverlay.classList.remove('opacity-100', 'pointer-events-auto');
            });
        }

        // Close sidebar when clicking outside on mobile or desktop
        if (overlay) {
            overlay.addEventListener('click', function() {
                if (sidebar.classList.contains('mobile-open')) {
                    sidebar.classList.remove('mobile-open');
                    sidebar.classList.add('mobile-closed');
                    overlay.classList.remove('active');
                } else if (sidebar.classList.contains('desktop-open')) {
                    sidebar.classList.remove('desktop-open');
                    sidebar.classList.add('desktop-closed');
                    overlay.classList.remove('active');
                }
            });
        }

        // Toggle notification dropdown
        if (notificationButton) {
            notificationButton.addEventListener('click', function(e) {
                e.stopPropagation();
                const isVisible = notificationDropdown.style.display === 'block';
                notificationDropdown.style.display = isVisible ? 'none' : 'block';
                if (userDropdown) userDropdown.style.display = 'none';
                // Close chat sidebar when notification dropdown is opened
                if (chatSidebar) chatSidebar.style.transform = 'translateX(100%)';
                if (chatOverlay) chatOverlay.classList.remove('opacity-100', 'pointer-events-auto');
            });
        }

        // Toggle user menu dropdown
        if (userMenuButton) {
            userMenuButton.addEventListener('click', function(e) {
                e.stopPropagation();
                const isVisible = userDropdown.style.display === 'block';
                userDropdown.style.display = isVisible ? 'none' : 'block';
                if (notificationDropdown) notificationDropdown.style.display = 'none';
                // Close chat sidebar when user dropdown is opened
                if (chatSidebar) chatSidebar.style.transform = 'translateX(100%)';
                if (chatOverlay) chatOverlay.classList.remove('opacity-100', 'pointer-events-auto');
            });
        }

        // Toggle chat sidebar with smooth transitions
        if (chatButton) {
            chatButton.addEventListener('click', function(e) {
                e.stopPropagation();
                const isVisible = chatSidebar.style.transform === 'translateX(0px)' ||
                                 chatSidebar.classList.contains('visible');

                if (isVisible) {
                    // Close the chat sidebar with smooth transition
                    chatSidebar.style.opacity = '0';
                    chatSidebar.style.transform = 'translateX(100%)';
                    chatOverlay.style.opacity = '0';

                    // Wait for transition to complete before hiding elements
                    setTimeout(() => {
                        chatSidebar.classList.remove('visible');
                        chatSidebar.classList.add('hidden');
                        chatOverlay.classList.remove('pointer-events-auto');
                        chatOverlay.classList.add('hidden');
                    }, 300); // Match transition duration
                } else {
                    // First make elements visible but transparent
                    chatSidebar.classList.remove('hidden');
                    chatSidebar.classList.add('visible');
                    chatSidebar.style.opacity = '0';
                    chatSidebar.style.transform = 'translateX(100%)';
                    chatOverlay.classList.remove('hidden');
                    chatOverlay.style.opacity = '0';

                    // Force browser to recognize the elements before animating
                    setTimeout(() => {
                        // Then animate them in
                        chatSidebar.style.opacity = '1';
                        chatSidebar.style.transform = 'translateX(0)';
                        chatOverlay.style.opacity = '1';
                        chatOverlay.classList.add('pointer-events-auto');

                        // Close other dropdowns
                        if (notificationDropdown) notificationDropdown.style.display = 'none';
                        if (userDropdown) userDropdown.style.display = 'none';

                        // Scroll to bottom of chat messages
                        if (chatMessages) {
                            chatMessages.scrollTop = chatMessages.scrollHeight;
                        }
                    }, 10);
                }
            });
        }

        // Close chat sidebar with close button - with smooth transition
        if (closeChatButton) {
            closeChatButton.addEventListener('click', function() {
                // Animate out
                chatSidebar.style.opacity = '0';
                chatSidebar.style.transform = 'translateX(100%)';
                chatOverlay.style.opacity = '0';

                // Wait for transition to complete before hiding elements
                setTimeout(() => {
                    chatSidebar.classList.remove('visible');
                    chatSidebar.classList.add('hidden');
                    chatOverlay.classList.remove('pointer-events-auto');
                    chatOverlay.classList.add('hidden');
                }, 300); // Match transition duration
            });
        }

        // Close chat sidebar when clicking overlay - with smooth transition
        if (chatOverlay) {
            chatOverlay.addEventListener('click', function() {
                // Animate out
                chatSidebar.style.opacity = '0';
                chatSidebar.style.transform = 'translateX(100%)';
                chatOverlay.style.opacity = '0';

                // Wait for transition to complete before hiding elements
                setTimeout(() => {
                    chatSidebar.classList.remove('visible');
                    chatSidebar.classList.add('hidden');
                    chatOverlay.classList.remove('pointer-events-auto');
                    chatOverlay.classList.add('hidden');
                }, 300); // Match transition duration
            });
        }

        // Close dropdowns when clicking elsewhere
        document.addEventListener('click', function() {
            if (notificationDropdown) notificationDropdown.style.display = 'none';
            if (userDropdown) userDropdown.style.display = 'none';
        });

        // Toggle between chat and users tabs
        if (chatTabButton && usersTabButton) {
            // Let HTMX handle the tab switching
            // We'll just add some additional behavior after the HTMX request completes

            document.body.addEventListener('htmx:afterSwap', function(event) {
                // Check if the event target is the chat content wrapper
                if (event.detail.target.id === 'chat-content-wrapper') {
                    // Scroll to bottom of chat messages if chat tab is active
                    const chatMessages = document.getElementById('chat-messages');
                    if (chatMessages && chatMessages.parentElement.style.display !== 'none') {
                        chatMessages.scrollTop = chatMessages.scrollHeight;
                    }
                }
            });
        }

        // Handle chat input and form submission
        if (chatForm && chatMessageInput) {
            // Enable/disable send button based on input
            chatMessageInput.addEventListener('input', function() {
                const messageText = this.value.trim();
                const sendButton = document.getElementById('send-message-button');

                if (sendButton) {
                    if (messageText) {
                        sendButton.removeAttribute('disabled');
                    } else {
                        sendButton.setAttribute('disabled', 'true');
                    }
                }
            });

            chatForm.addEventListener('submit', function(e) {
                e.preventDefault();

                const messageText = chatMessageInput.value.trim();
                if (!messageText) return;

                // Create a new message element
                const messageTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                const messageHTML = `
                    <div class="chat-message current-user" id="message-new">
                        <div class="message-avatar-container">
                            <img src="/img/code-avatar.svg" alt="DeadDev_42's avatar" class="message-avatar">
                        </div>
                        <div class="message-content">
                            <div class="message-header">
                                <span class="message-sender">DeadDev_42</span>
                                <span class="user-status-text online">online</span>
                                <span class="message-time">${messageTime}</span>
                            </div>
                            <p class="message-text">${messageText}</p>
                        </div>
                    </div>
                `;

                // Add message to chat
                const messageDiv = document.createElement('div');
                messageDiv.innerHTML = messageHTML;
                // Extract the actual message element from the wrapper
                const messageElement = messageDiv.firstElementChild;
                chatMessages.appendChild(messageElement);

                // Clear input and scroll to bottom
                chatMessageInput.value = '';

                // Disable send button again
                const sendButton = document.getElementById('send-message-button');
                if (sendButton) {
                    sendButton.setAttribute('disabled', 'true');
                }

                // Scroll to bottom of messages
                const messagesEnd = document.createElement('div');
                chatMessages.appendChild(messagesEnd);
                messagesEnd.scrollIntoView({ behavior: 'smooth' });
            });
        }

        // Close dropdowns when clicking elsewhere
        document.addEventListener('click', function() {
            if (notificationDropdown) notificationDropdown.style.display = 'none';
            if (userDropdown) userDropdown.style.display = 'none';
        });
    });
    """

# Sidebar component
def Sidebar(username, active_tab, is_mobile, sidebar_open):
    return Aside(
        Div(
            # Logo is wrapped in sidebar-content for visibility toggle
            Div(
                H1("DeadDev", Span("Hub", cls="logo-accent"), cls="logo"),
                cls="sidebar-content"
            ),
            Button(MenuIcon(), cls="sidebar-toggle", id="sidebar-toggle"),
            cls="sidebar-header"
        ),
        Nav(
            Ul(
                Li(
                    Button(
                        HomeIcon(),
                        Span("Dashboard", cls="sidebar-content", id="dashboard-label"),
                        cls=f"nav-item {'active' if active_tab == 'dashboard' else ''}",
                        hx_post="/toggle_tab",
                        hx_vals='{"tab": "dashboard"}',
                        hx_target="body",
                        hx_swap="none"
                    )
                ),
                Li(
                    Button(
                        ProjectsIcon(),
                        Span("Projects", cls="sidebar-content", id="projects-label"),
                        cls=f"nav-item {'active' if active_tab == 'projects' else ''}",
                        hx_post="/toggle_tab",
                        hx_vals='{"tab": "projects"}',
                        hx_target="body",
                        hx_swap="none"
                    )
                ),
                Li(
                    Button(
                        AnalyticsIcon(),
                        Span("Analytics", cls="sidebar-content", id="analytics-label"),
                        cls=f"nav-item {'active' if active_tab == 'analytics' else ''}",
                        hx_post="/toggle_tab",
                        hx_vals='{"tab": "analytics"}',
                        hx_target="body",
                        hx_swap="none"
                    )
                ),
                Li(
                    Button(
                        TeamIcon(),
                        Span("Team", cls="sidebar-content", id="team-label"),
                        cls=f"nav-item {'active' if active_tab == 'team' else ''}",
                        hx_post="/toggle_tab",
                        hx_vals='{"tab": "team"}',
                        hx_target="body",
                        hx_swap="none"
                    )
                ),
                Li(
                    Button(
                        DocsIcon(),
                        Span("Documentation", cls="sidebar-content", id="docs-label"),
                        cls=f"nav-item {'active' if active_tab == 'docs' else ''}",
                        hx_post="/toggle_tab",
                        hx_vals='{"tab": "docs"}',
                        hx_target="body",
                        hx_swap="none"
                    )
                ),
                cls="nav-list"
            ),
            
            # Recent Projects (shown when sidebar is expanded)
            Div(
                H3("Recent Projects", cls="recent-projects-title"),
                Ul(
                    Li(
                        A(
                            Span(cls="project-dot python"),
                            "AI Code Generator",
                            href="#",
                            cls="recent-project-item"
                        )
                    ),
                    Li(
                        A(
                            Span(cls="project-dot javascript"),
                            "DeadBot",
                            href="#",
                            cls="recent-project-item"
                        )
                    ),
                    Li(
                        A(
                            Span(cls="project-dot git"),
                            "GitSync",
                            href="#",
                            cls="recent-project-item"
                        )
                    ),
                    cls="recent-projects-list"
                ),
                cls="recent-projects sidebar-content"
            ),
            cls="sidebar-nav"
        ),
        
        # Sidebar Footer
        Div(
            Button(
                SettingsIcon(),
                Span("Settings", cls="sidebar-content", id="settings-label"),
                cls=f"nav-item {'active' if active_tab == 'settings' else ''}",
                hx_post="/toggle_tab",
                hx_vals='{"tab": "settings"}',
                hx_target="body",
                hx_swap="none"
            ),
            cls="sidebar-footer"
        ),
        
        id="sidebar",
        cls=f"sidebar {is_mobile and (sidebar_open and 'mobile-open' or 'mobile-closed') or (sidebar_open and 'desktop-open' or 'desktop-closed')}"
    )

# Header component
def Header(left_content, right_content):
    return Div(
        left_content,
        right_content,
        cls="header"
    )

# Dashboard layout component that combines header and sidebar
def DashboardLayout(username, state, content):
    is_mobile = state.get('isMobile', False)
    sidebar_open = state.get('sidebarOpen', False)
    active_tab = state.get('activeTab', 'dashboard')

    # Create header left content
    header_left = Div(
        Button(
            MenuIcon(),
            cls="menu-button",
            id="menu-button"
        ),
        Div(
            Div(
                SearchIcon(),
                cls="search-icon"
            ),
            Input(
                type="text",
                placeholder="Search projects, docs, or users...",
                cls="search-input",
                value=state.get('searchQuery', ''),
                id="search-input"
            ),
            cls="search-container"
        ),
        cls="header-left"
    )

    # Create header right content
    header_right = Div(
    Button(MessageSquareIcon(), cls="chat-button", id="chat-button"),
        Div(
            Button(
                NotificationIcon(),
                Span("3", cls="notification-badge"),
                cls="notification-button",
                id="notification-button"
            ),
            # Notification Dropdown
            Div(
                Div(
                    H3("Notifications"),
                    Button("Mark all as read", cls="mark-read-button"),
                    cls="notification-header"
                ),
                Div(
                    Div(
                        Div(
                            TeamNotificationIcon(),
                            cls="notification-icon team"
                        ),
                        Div(
                            P(
                                Span("TeamSync", cls="bold"),
                                " invited you to collaborate"
                            ),
                            P("2 minutes ago", cls="notification-time"),
                            cls="notification-content"
                        ),
                        cls="notification-item flex items-center"
                    ),
                    Div(
                        Div(
                            StarIconNotification(),
                            cls="notification-icon star"
                        ),
                        Div(
                            P(
                                Span("DeadBot", cls="bold"),
                                " received 5 new stars"
                            ),
                            P("1 hour ago", cls="notification-time"),
                            cls="notification-content"
                        ),
                        cls="notification-item flex items-center"
                    ),
                    Div(
                        Div(
                            MessageIcon(),
                            cls="notification-icon message"
                        ),
                        Div(
                            P(
                                Span("AI Code Generator", cls="bold"),
                                " new comment from ",
                                Span("user123", cls="bold")
                            ),
                            P("Yesterday", cls="notification-time"),
                            cls="notification-content"
                        ),
                        cls="notification-item flex items-center"
                    ),
                    cls="notification-list"
                ),
                Div(
                    Button("View all notifications", cls="view-all-button"),
                    cls="notification-footer"
                ),
                cls="notification-dropdown",
                id="notification-dropdown",
                style="display: none;"
            ),
            cls="notification-container"
        ),
        Div(
            Button(
                Div(
                    Img(src="\img\code-avatar.svg?height=32&width=32",
                        alt="Profile",
                        crossorigin="anonymous",
                        cls="avatar"
                    ),
                    cls="avatar-container"
                ),
                Span(username, cls="username"),
                cls="user-menu-button",
                id="user-menu-button",
                # Adding HTMX attributes for dropdown toggle
                hx_target="#user-dropdown",
                hx_swap="innerHTML"
            ),

            # User Dropdown
            Div(
                Div(
                    P(username, cls="user-name"),
                    P("Senior AI Developer", cls="user-role"),
                    cls="user-dropdown-header"
                ),
                Ul(
                    Li(
                        A(
                            EditProfileIcon(),
                            "Edit Profile",
                            href="#",
                            cls="user-dropdown-item"
                        ),
                        style="list-style: none;"
                    ),
                    Li(
                        A(
                            BillingIcon(),
                            "Billing",
                            href="#",
                            cls="user-dropdown-item"
                        ),
                        style="list-style: none;"
                    ),
                    Li(
                        A(
                            SecurityIcon(),
                            "Security",
                            href="#",
                            cls="user-dropdown-item"
                        ),
                        style="list-style: none;"
                    ),
                    Li(
                        A(
                            SignOutIcon(),
                            "Sign Out",
                            href="#",
                            cls="user-dropdown-item"
                        ),
                        cls="dropdown-divider",
                        style="list-style: none;"
                    ),
                    cls="user-dropdown-menu"
                ),
                cls="user-dropdown",
                id="user-dropdown",
                style="display: none;"  # Consider handling visibility with CSS/JS instead
            ),
            cls="user-menu-container"
        ),
        GlobalChat(),
        cls="header-right"
    )

    return Div(
        # Overlay when sidebar is open
        Div(cls=f"sidebar-overlay {'active' if sidebar_open and is_mobile else ''}", id="sidebar-overlay"),

        # Sidebar
        Sidebar(username, active_tab, is_mobile, sidebar_open),

        # Main Content
        Div(
            # Header
            Header(header_left, header_right),

            # Main Dashboard Content
            Main(
                content,
                cls="dashboard-main"
            ),
            cls="main-content"
        ),
        cls="dashboard-container dashboard-page"
    )

# Route handler for sending messages

@rt('/chat_send', methods=['POST'])
async def chat_send_message(request):
    """
    Route handler for sending a message in the chat.
    This endpoint is called via fetch API when a message is submitted.
    """
    # In a real application, you would save the message to a database
    # and potentially broadcast it to other users via WebSockets

    # For now, we'll just return a new message element
    try:
        # Get form data
        form_data = await request.form()
        message_text = form_data.get('message', '')

        if not message_text:
            return ""

        # Create a timestamp for the message
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M")

        # Use a default username
        username = "You"
    except Exception as e:
        # If there's an error, return a message about it
        return Div(f"Error sending message: {str(e)}", cls="error-message")

    # Return a new message element
    return Div(
        Div(
            Img(src="\img\code-avatar.svg", alt=f"{username}'s avatar", cls="message-avatar"),
            cls="message-avatar-container"
        ),
        Div(
            Div(
                Span(username, cls="message-sender"),
                Span("online", cls="user-status-text online"),
                Span(timestamp, cls="message-time"),
                cls="message-header"
            ),
            P(message_text, cls="message-text"),
            cls="message-content"
        ),
        cls="chat-message current-user",
        id=f"message-new-{int(datetime.now().timestamp())}"
    )