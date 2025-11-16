"""
Helper functions for generating feed content
This eliminates code duplication in the main.py scrolling feeds
"""

from fasthtml.common import *


def generate_live_updates():
    """Generate the list of live update items (used for infinite scroll)"""
    updates = [
        ("@sarah", " completed the daily challenge using AI pair programming"),
        ("@maya", " deployed a new feature in 0.3s with AI assistance"),
        ("@chris", " optimized database queries using AI suggestions"),
        ("@taylor", " created a responsive layout with AI pair programming"),
        ("@jordan", " automated testing with AI-generated test cases"),
        ("@quinn", " improved API documentation using AI"),
        ("@riley", " fixed 3 bugs with AI code analysis"),
    ]
    
    items = []
    for username, activity in updates:
        items.append(
            Li(
                Span(username, cls="username"),
                activity,
                cls="update-item"
            )
        )
    
    return items


def generate_live_feed():
    """Generate the list of live feed items (blog posts and announcements)"""
    feed_items = [
        ("📢 ANNOUNCEMENT", " AI Code Challenge Week starts Monday! Get ready to compete! 🏆", "announcement-item"),
        ("@sophia", " published: 'Building Scalable Systems with AI'", ""),
        ("@marcus", " posted: 'From Junior to Senior with AI in 6 Months'", ""),
        ("@elena", " wrote: 'The Ultimate Guide to AI Prompt Engineering'", ""),
        ("📢 ANNOUNCEMENT", " New AI Pairing Features Released! 🚀", "announcement-item"),
        ("@kai", " published: 'AI-First Architecture Patterns That Scale'", ""),
        ("@zara", " shared: 'My Journey to 90% AI Development'", ""),
        ("📢 ANNOUNCEMENT", " Community Milestone - 10k Members! 🎉", "announcement-item"),
        ("@lucas", " wrote: 'Revolutionizing Code Reviews with AI'", ""),
    ]
    
    items = []
    for user_or_tag, content, extra_class in feed_items:
        if user_or_tag.startswith("📢"):
            items.append(
                Li(
                    Span(user_or_tag, cls="announcement"),
                    content,
                    cls=f"feed-item {extra_class}".strip()
                )
            )
        else:
            items.append(
                Li(
                    Span(user_or_tag, cls="username"),
                    content,
                    cls="feed-item"
                )
            )
    
    return items


def create_scrolling_feed(items, feed_class="updates-list"):
    """
    Create a scrolling feed with duplicated items for infinite scroll effect
    
    Args:
        items: List of Li elements to display
        feed_class: CSS class for the feed container
    
    Returns:
        Ul element with items duplicated for smooth infinite scrolling
    """
    # Duplicate items for smooth scrolling effect
    return Ul(*items, *items, cls=feed_class)
