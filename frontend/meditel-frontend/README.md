# Meditel Healthcare Appointment System

A modern healthcare management system built with React, TypeScript, and Tailwind CSS.

## Features
- 🏥 Appointment scheduling and management
- 👨‍⚕️ Doctor directory and profiles
- 👤 Patient records and symptoms tracking
- 📅 Interactive calendar and scheduling
- 🔍 Real-time search and filtering
- 🎨 Modern, responsive UI with Tailwind CSS
- 📱 Mobile-friendly design

## Quick Start

### Option 1: Automatic Setup (Windows)
1. Double-click \`setup.bat\`
2. Wait for installation to complete
3. Open browser to \`http://localhost:3000\`

### Option 2: Automatic Setup (Mac/Linux)
\`\`\`bash
chmod +x setup.sh
./setup.sh
\`\`\`

### Option 3: Manual Setup
\`\`\`bash
# Install dependencies
npm install

# Start development server
npm run dev

# Open http://localhost:3000
\`\`\`

## Project Structure
\`\`\`
meditel-app/
├── src/
│   ├── App.tsx          # Main application component
│   ├── main.tsx         # Application entry point
│   └── index.css        # Tailwind CSS imports
├── public/              # Static assets
├── package.json         # Dependencies and scripts
├── vite.config.ts       # Vite configuration
├── tailwind.config.js   # Tailwind CSS configuration
└── README.md           # This file
\`\`\`

## Technologies Used
- **React 18** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling framework
- **Vite** - Build tool and dev server
- **Lucide React** - Icon library

## Mock Data
The app includes sample data for:
- 4 doctors with different specialties
- 4 patients with various symptoms
- 4 sample appointments

All CRUD operations work with local state - no backend required!

## Customization
- Edit \`src/App.tsx\` to modify the application
- Update \`tailwind.config.js\` for custom styling
- Change mock data in the component state

## License
MIT - Free to use and modify