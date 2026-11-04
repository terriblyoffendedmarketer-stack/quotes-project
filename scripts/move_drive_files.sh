#!/usr/bin/env bash
# scripts/move_drive_files.sh — Server-side moves tactical lead magnets and HBR books on Google Drive
# Usage: bash scripts/move_drive_files.sh
# Requires: rclone configured with 'gdrive:'
set -euo pipefail

echo '=== Creating Target Folders on Google Drive ==='
rclone mkdir "gdrive:Books/Archive of bullshit"
rclone mkdir "gdrive:Books/HBR"

echo '=== Moving Tactical Lead Magnets & Whitepapers to Archive of bullshit ==='
rclone moveto "gdrive:Books/Cooking and food/DamianTheFatass - CookBook of Gains.pdf" "gdrive:Books/Archive of bullshit/DamianTheFatass - CookBook of Gains.pdf"
rclone moveto "gdrive:Books/Others/Instantly - How We Get 400+ Replies Monthly With Our Cold Email Copywriting Framework .docx" "gdrive:Books/Archive of bullshit/Instantly - How We Get 400+ Replies Monthly With Our Cold Email Copywriting Framework .docx"
rclone moveto "gdrive:Books/Others/Mr Beast - How-To-Succeed-At-MrBeast-Production.pdf" "gdrive:Books/Archive of bullshit/Mr Beast - How-To-Succeed-At-MrBeast-Production.pdf"
rclone moveto "gdrive:Books/Others/Product Marketing Glossary - V2.pdf" "gdrive:Books/Archive of bullshit/Product Marketing Glossary - V2.pdf"
rclone moveto "gdrive:Books/Others/The LinkedIn Engagement Routine.pdf" "gdrive:Books/Archive of bullshit/The LinkedIn Engagement Routine.pdf"
rclone moveto "gdrive:Books/Others/LinkedIn content strategy system.pdf" "gdrive:Books/Archive of bullshit/LinkedIn content strategy system.pdf"
rclone moveto "gdrive:Books/Others/9 Tips For Your Messaging Strategy.pdf" "gdrive:Books/Archive of bullshit/9 Tips For Your Messaging Strategy.pdf"
rclone moveto "gdrive:Books/Others/Sell like crazy - Sabri Suby.pdf" "gdrive:Books/Archive of bullshit/Sell like crazy - Sabri Suby.pdf"
rclone moveto "gdrive:Books/Others/Total Posture Mobility MBD.pdf" "gdrive:Books/Archive of bullshit/Total Posture Mobility MBD.pdf"
rclone moveto "gdrive:Books/Others/Total Shoulder Mobility 2.0.pdf.pdf" "gdrive:Books/Archive of bullshit/Total Shoulder Mobility 2.0.pdf.pdf"
rclone moveto "gdrive:Books/Others/72 Viral Linkedin Post Breakdown.pdf" "gdrive:Books/Archive of bullshit/72 Viral Linkedin Post Breakdown.pdf"
rclone moveto "gdrive:Books/Others/Dawn Creative - Ulitmate Brand Strategy Toolkit.pdf" "gdrive:Books/Archive of bullshit/Dawn Creative - Ulitmate Brand Strategy Toolkit.pdf"
rclone moveto "gdrive:Books/Others/Cold-Email-Templates.pdf" "gdrive:Books/Archive of bullshit/Cold-Email-Templates.pdf"
rclone moveto "gdrive:Books/Others/A Step-by-Step Guide to Improve Email Performance - Mailmodo.pdf" "gdrive:Books/Archive of bullshit/A Step-by-Step Guide to Improve Email Performance - Mailmodo.pdf"
rclone moveto "gdrive:Books/Others/CopyBlogger - Content Marketing Research - The Crucial 1st Step.pdf" "gdrive:Books/Archive of bullshit/CopyBlogger - Content Marketing Research - The Crucial 1st Step.pdf"
rclone moveto "gdrive:Books/Others/The 5 P Approach to Copy That Crushes it - Copyblogger.pdf" "gdrive:Books/Archive of bullshit/The 5 P Approach to Copy That Crushes it - Copyblogger.pdf"
rclone moveto "gdrive:Books/Others/Your Free SEO Search Intent Framework.pdf" "gdrive:Books/Archive of bullshit/Your Free SEO Search Intent Framework.pdf"
rclone moveto "gdrive:Books/Others/Email Subject Line Ebook - Mailmodo & Ekaterina V2.0.pdf" "gdrive:Books/Archive of bullshit/Email Subject Line Ebook - Mailmodo & Ekaterina V2.0.pdf"
rclone moveto "gdrive:Books/Others/The Product Strategy Playbook by ProductPlan.pdf" "gdrive:Books/Archive of bullshit/The Product Strategy Playbook by ProductPlan.pdf"
rclone moveto "gdrive:Books/Others/Dave Garehardt Copywriting.pptx" "gdrive:Books/Archive of bullshit/Dave Garehardt Copywriting.pptx"
rclone moveto "gdrive:Books/Others/Copyblogger - Copywriting-101 How to Craft-Compelling Copy.pdf" "gdrive:Books/Archive of bullshit/Copyblogger - Copywriting-101 How to Craft-Compelling Copy.pdf"
rclone moveto "gdrive:Books/Others/Liz Ellits - How to Get Benchmark-Busting  Email Open Rates.pdf" "gdrive:Books/Archive of bullshit/Liz Ellits - How to Get Benchmark-Busting  Email Open Rates.pdf"
rclone moveto "gdrive:Books/Tactical Marketing/What the Fortune 500 Read.pdf" "gdrive:Books/Archive of bullshit/What the Fortune 500 Read.pdf"
rclone moveto "gdrive:Books/Tactical Marketing/Alex Hormozi - 100M offers .epub" "gdrive:Books/Archive of bullshit/Alex Hormozi - 100M offers .epub"
rclone moveto "gdrive:Books/Tactical Marketing/Jordan Belfort - Way of the Wolf_ Straight Line Selling_ Master the Art of Persuasion, Influence, and Success.pdf" "gdrive:Books/Archive of bullshit/Jordan Belfort - Way of the Wolf_ Straight Line Selling_ Master the Art of Persuasion, Influence, and Success.pdf"
rclone moveto "gdrive:Books/Tactical Marketing/Scorecard Marketing - Daniel Priestley.pdf" "gdrive:Books/Archive of bullshit/Scorecard Marketing - Daniel Priestley.pdf"
rclone moveto "gdrive:Books/Tactical Marketing/WorldClassPricingTheJourney.pdf" "gdrive:Books/Archive of bullshit/WorldClassPricingTheJourney.pdf"
rclone moveto "gdrive:Books/Tactical Marketing/The ABM Cookbook - Terminus.pdf" "gdrive:Books/Archive of bullshit/The ABM Cookbook - Terminus.pdf"
rclone moveto "gdrive:Books/Tactical Marketing/The 60 Second Sale.epub" "gdrive:Books/Archive of bullshit/The 60 Second Sale.epub"
rclone moveto "gdrive:Books/Tactical Marketing/Secret Sauce The Ultimate Growth Hacking Guide.epub" "gdrive:Books/Archive of bullshit/Secret Sauce The Ultimate Growth Hacking Guide.epub"

echo '=== Moving Harvard Business Review Books to Books/HBR ==='
rclone moveto "gdrive:Books/Fiction ／ non fiction/HBR on Persuasive Presentations.pdf" "gdrive:Books/HBR/HBR on Persuasive Presentations.pdf"
rclone moveto "gdrive:Books/Fiction ／ non fiction/HBR On communication" "gdrive:Books/HBR/HBR On communication"
rclone moveto "gdrive:Books/Tactical Marketing/Harvard Innovation Labs_ Product-Market Fit.pdf" "gdrive:Books/HBR/Harvard Innovation Labs_ Product-Market Fit.pdf"
rclone moveto "gdrive:Books/Tactical Marketing/HBR On Strategic Marketing.pdf" "gdrive:Books/HBR/HBR On Strategic Marketing.pdf"

echo '=== All moves completed successfully! ==='
