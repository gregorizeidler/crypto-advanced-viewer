"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion } from "framer-motion";
import {
  LayoutDashboard,
  TrendingUp,
  Microscope,
  Wrench,
  Activity,
} from "lucide-react";

const menuItems = [
  { href: "/", label: "Dashboard Principal", icon: LayoutDashboard },
  { href: "/analise", label: "Análise Técnica", icon: TrendingUp },
  { href: "/analise-avancada", label: "Análises Avançadas", icon: Microscope },
  { href: "/ferramentas", label: "Ferramentas", icon: Wrench },
];

export default function NavigationSidebar() {
  const pathname = usePathname();

  return (
    <div className="fixed left-0 top-0 h-screen w-64 glass border-r border-gray-800 p-6 z-50 bg-black/80 backdrop-blur-xl">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <Activity className="w-8 h-8 text-blue-500" />
          <h2 className="text-xl font-bold text-white">Crypto Viewer</h2>
        </div>
        <p className="text-xs text-gray-400">Advanced Crypto Analysis</p>
      </div>

      <nav className="space-y-2">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href;

          return (
            <Link key={item.href} href={item.href}>
              <motion.div
                whileHover={{ x: 4 }}
                whileTap={{ scale: 0.98 }}
                className={`
                  w-full flex items-center gap-3 px-4 py-3 rounded-lg
                  transition-all duration-200 cursor-pointer
                  ${
                    isActive
                      ? "bg-blue-600 text-white shadow-lg shadow-blue-600/50"
                      : "text-gray-400 hover:text-white hover:bg-gray-800"
                  }
                `}
              >
                <Icon className="w-5 h-5" />
                <span className="font-medium">{item.label}</span>
              </motion.div>
            </Link>
          );
        })}
      </nav>

      <div className="absolute bottom-6 left-6 right-6">
        <div className="glass rounded-lg p-4 bg-gray-900/50">
          <div className="flex items-center gap-2 mb-2">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-xs text-gray-400">Real-time data</span>
          </div>
          <p className="text-xs text-gray-500">
            20+ Advanced Analyses
          </p>
        </div>
      </div>
    </div>
  );
}

