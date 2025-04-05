from fasthtml.common import *
from fasthtml.svg import Svg, ft_svg as tag
from pathlib import Path
import json
from typing import Dict, List

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
        strokeWidth="2", fill="none"
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
                Div(cls="avatar-status online") if msg["user"]["online"] else None,
                cls="message-avatar-container"
            ),
            Div(
                Div(
                    Span(msg["user"]["name"], cls="message-sender"),
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
                cls="user-avatar-container"
            ),
            Div(
                Div(
                    Span(user["name"], cls="user-name"),
                    Span(user["status"], cls="user-status-text"),
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
        # Chat overlay
        Div(
            cls=f"chat-overlay {'opacity-100 pointer-events-auto' if is_open else 'hidden'}",
            id="chat-overlay",
            hx_swap_oob="true"
        ),

        # Chat sidebar
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
                        cls="chat-tab-content"
                    ),
                    cls="chat-tab active",
                    id="chat-tab-button",
                    hx_get="/chat_tab",  # Dummy endpoint for tab switch
                    hx_target="#chat-content",
                    hx_swap="innerHTML"
                ),
                Button(
                    Div(
                        UsersIcon(width=16, height=16),
                        Span("Users"),
                        cls="chat-tab"
                    ),
                    cls="chat-tab",
                    id="users-tab-button",
                    hx_get="/users_tab",  # Dummy endpoint for tab switch
                    hx_target="#users-content",
                    hx_swap="innerHTML"
                ),
                cls="chat-tabs"
            ),

            # Content
            Div(
                # Messages tab
                Div(
                    Div(
                        *message_elements,
                        id="chat-messages",
                        cls="chat-messages"
                    ),
                    Div(
                        Form(
                            Input(
                                type="text",
                                placeholder="Type a message...",
                                cls="chat-input",
                                id="chat-message-input",
                                name="message"
                            ),
                            Button(
                                SendIcon(),
                                type="submit",
                                cls="chat-send-button",
                                id="send-message-button",
                                disabled=True
                            ),
                            hx_post="/send_message",
                            hx_target="#chat-messages",
                            hx_swap="beforeend",
                            cls="chat-input-form",
                            id="chat-form"
                        ),
                        cls="chat-input-container"
                    ),
                    id="chat-content",
                    cls="chat-content",
                    style="display: flex;"
                ),

                # Users tab
                Div(
                    *user_elements,
                    id="users-content",
                    cls="users-list",
                    style="display: none;"
                ),

                cls="chat-content-wrapper"
            ),

            cls=f"chat-sidebar {'visible' if is_open else 'hidden'}",
            id="chat-sidebar",
            style=f"transform: translateX({'0' if is_open else '100%'});"
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

        // Mobile menu button
        if (chatButton) {
        chatButton.addEventListener('click', function(e) {
            e.stopPropagation();
            const isVisible = chatSidebar.style.transform === 'translateX(0px)';
            if (isVisible) {
                chatSidebar.style.transform = 'translateX(100%)';
                chatOverlay.classList.remove('opacity-100', 'pointer-events-auto');
            } else {
                chatSidebar.style.transform = 'translateX(0)';
                chatOverlay.classList.add('opacity-100', 'pointer-events-auto');
                // Close other dropdowns
                if (notificationDropdown) notificationDropdown.style.display = 'none';
                if (userDropdown) userDropdown.style.display = 'none';
                // Scroll to bottom
                if (chatMessages) chatMessages.scrollTop = chatMessages.scrollHeight;
            }
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

        // Toggle chat sidebar
        if (chatButton) {
            chatButton.addEventListener('click', function(e) {
                e.stopPropagation();
                const isVisible = chatSidebar.style.transform === 'translateX(0px)';

                if (isVisible) {
                    chatSidebar.style.transform = 'translateX(100%)';
                    chatOverlay.classList.remove('opacity-100', 'pointer-events-auto');
                } else {
                    chatSidebar.style.transform = 'translateX(0)';
                    chatOverlay.classList.add('opacity-100', 'pointer-events-auto');

                    // Close other dropdowns
                    if (notificationDropdown) notificationDropdown.style.display = 'none';
                    if (userDropdown) userDropdown.style.display = 'none';

                    // Scroll to bottom of chat messages
                    if (chatMessages) {
                        chatMessages.scrollTop = chatMessages.scrollHeight;
                    }
                }
            });
        }

        // Close chat sidebar with close button
        if (closeChatButton) {
            closeChatButton.addEventListener('click', function() {
                chatSidebar.style.transform = 'translateX(100%)';
                chatOverlay.classList.remove('opacity-100', 'pointer-events-auto');
            });
        }

        // Close chat sidebar when clicking overlay
        if (chatOverlay) {
            chatOverlay.addEventListener('click', function() {
                chatSidebar.style.transform = 'translateX(100%)';
                chatOverlay.classList.remove('opacity-100', 'pointer-events-auto');
            });
        }

        // Toggle between chat and users tabs
        if (chatTabButton && usersTabButton) {
            chatTabButton.addEventListener('click', function(e) {
                e.preventDefault();
                chatContent.style.display = 'flex';
                usersContent.style.display = 'none';
                chatTabButton.classList.add('active');
                usersTabButton.classList.remove('active');
                document.querySelector('#chat-sidebar h2').textContent = "Global Chat";
                htmx.trigger(chatTabButton, 'htmx:trigger');
            });

            usersTabButton.addEventListener('click', function(e) {
                e.preventDefault();
                chatContent.style.display = 'none';
                usersContent.style.display = 'block';
                usersTabButton.classList.add('active');
                chatTabButton.classList.remove('active');
                document.querySelector('#chat-sidebar h2').textContent = "Online Users";
                htmx.trigger(usersTabButton, 'htmx:trigger');
            });


            usersTabButton.addEventListener('click', function() {
                if (activeTab !== "users") {
                    activeTab = "users";

                    // Update tab styling
                    usersTabButton.classList.add('text-[#00ff00]', 'border-b-2', 'border-[#00ff00]');
                    usersTabButton.classList.remove('text-gray-400', 'hover:text-white');

                    chatTabButton.classList.remove('text-[#00ff00]', 'border-b-2', 'border-[#00ff00]');
                    chatTabButton.classList.add('text-gray-400', 'hover:text-white');

                    // Show users content
                    document.getElementById('chat-content').style.display = 'none';
                    document.getElementById('users-content').style.display = 'block';

                    // Update header text
                    const headerText = document.querySelector('#chat-sidebar h2');
                    if (headerText) headerText.textContent = "Online Users";
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
                    <div class="flex gap-3">
                        <div class="flex-shrink-0">
                            <div class="relative">
                                <img src="/img/code-avatar.svg?height=32&width=32" alt="DeadDev_42" class="w-8 h-8 rounded-full bg-[#252525]">
                                <div class="absolute bottom-0 right-0 w-2.5 h-2.5 bg-green-500 rounded-full border-2 border-[#1a1a1a]"></div>
                            </div>
                        </div>
                        <div class="flex-1">
                            <div class="flex items-center gap-2">
                                <span class="font-medium text-sm text-white">DeadDev_42</span>
                                <span class="text-xs text-gray-500">${messageTime}</span>
                            </div>
                            <p class="text-sm text-gray-300 mt-1">${messageText}</p>
                        </div>
                    </div>
                `;

                // Add message to chat
                const messageDiv = document.createElement('div');
                messageDiv.innerHTML = messageHTML;
                chatMessages.appendChild(messageDiv);

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
        GlobalChat(is_open=True),
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