import { useState } from "react";
import {
  House,
  Map,
  CalendarDays,
  Users,
  DoorOpen,
  Bell,
  UserRound,
  GraduationCap,
  Menu,
  X,
} from "lucide-react";
import { NavLink } from "react-router-dom";

const navItems = [
  { label: "Home", icon: House, to: "/teacher/dashboard" },
  { label: "Campus Map", icon: Map, to: "/campus-map" },
  { label: "My Timetable", icon: CalendarDays, to: "/teacher/timetable" },
  { label: "Teachers", icon: Users, to: "/teachers" },
  { label: "Rooms", icon: DoorOpen, to: "/rooms" },
  { label: "Notifications", icon: Bell, to: "/notifications" },
  { label: "Profile", icon: UserRound, to: "/teacher/profile" },
];

const mobileItems = navItems.filter((item) =>
  ["Home", "Campus Map", "My Timetable", "Notifications"].includes(item.label),
);

function SidebarLinks({ onNavigate }) {
  return (
    <nav className="flex-1 space-y-2 px-3 py-5">
      {navItems.map(({ label, icon: Icon, to }) => (
        <NavLink
          key={label}
          to={to}
          end={to === "/teacher/dashboard"}
          onClick={onNavigate}
          className={({ isActive }) =>
            `flex items-center gap-4 rounded-xl px-4 py-3
            transition-colors ${
              isActive
                ? "border border-[#593020] bg-[#321B15] text-[#FF642D]"
                : "text-slate-300 hover:bg-[#171B24] hover:text-white"
            }`
          }
        >
          <Icon size={22} />
          <span className="text-sm font-medium">{label}</span>
        </NavLink>
      ))}
    </nav>
  );
}

export default function DashboardSidebar() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <>
      {/* Desktop sidebar */}
      <aside
        className="hidden w-60 shrink-0 flex-col
        border-r border-[#242832] bg-[#080B11] text-white lg:flex"
      >
        <div className="flex h-20 items-center gap-3 px-5">
          <GraduationCap className="size-9 text-[#FF642D]" />
          <span className="text-xl font-bold">CampusFlow</span>
        </div>

        <SidebarLinks />

        <div
          className="m-3 rounded-xl border border-[#252A35]
          bg-[#111722] p-4"
        >
          <p className="font-semibold">CampusFlow</p>
          <p className="mt-2 text-sm text-slate-400">
            Find classes and teachers across your campus.
          </p>
        </div>
      </aside>

      {/* Mobile top bar */}
      <header
        className="flex h-16 shrink-0 items-center
        justify-between border-b border-[#242832]
        bg-[#080B11] px-4 text-white lg:hidden"
      >
        <div className="flex items-center gap-2">
          <GraduationCap className="size-8 text-[#FF642D]" />
          <span className="text-lg font-bold">CampusFlow</span>
        </div>

        <button
          type="button"
          onClick={() => setMenuOpen(true)}
          aria-label="Open navigation menu"
          aria-expanded={menuOpen}
          className="rounded-lg border border-[#252A35] p-2
            text-slate-200 hover:text-[#FF642D]"
        >
          <Menu size={23} />
        </button>
      </header>

      {/* Mobile drawer and backdrop */}
      {menuOpen && (
        <div className="fixed inset-0 z-50 lg:hidden">
          <button
            type="button"
            aria-label="Close navigation menu"
            onClick={() => setMenuOpen(false)}
            className="absolute inset-0 h-full w-full
              bg-black/70"
          />

          <aside
            className="absolute inset-y-0 left-0
            flex w-[min(82vw,300px)] flex-col
            border-r border-[#242832] bg-[#080B11]
            text-white shadow-2xl"
          >
            <div
              className="flex h-16 items-center
              justify-between border-b border-[#242832] px-5"
            >
              <span className="font-bold">Navigation</span>

              <button
                type="button"
                onClick={() => setMenuOpen(false)}
                aria-label="Close navigation menu"
                className="rounded-lg p-2 hover:bg-[#171B24]"
              >
                <X size={21} />
              </button>
            </div>

            <SidebarLinks onNavigate={() => setMenuOpen(false)} />

            <div
              className="m-3 rounded-xl border border-[#252A35]
              bg-[#111722] p-4"
            >
              <p className="font-semibold">CampusFlow</p>
              <p className="mt-2 text-sm text-slate-400">
                Your campus, connected.
              </p>
            </div>
          </aside>
        </div>
      )}

      {/* Mobile bottom navigation */}
      <nav
        className="fixed inset-x-0 bottom-0 z-40
        grid grid-cols-4 border-t border-[#242832]
        bg-[#080B11]/95 pb-[env(safe-area-inset-bottom)]
        backdrop-blur-md lg:hidden"
      >
        {mobileItems.map(({ label, icon: Icon, to }) => (
          <NavLink
            key={label}
            to={to}
            end={to === "/teacher/dashboard"}
            className={({ isActive }) =>
              `flex min-h-16 flex-col items-center
              justify-center gap-1 px-1 py-2 ${
                isActive ? "text-[#FF642D]" : "text-slate-400 hover:text-white"
              }`
            }
          >
            <Icon size={21} />
            <span className="text-[10px] font-medium sm:text-xs">
              {label === "My Timetable" ? "Timetable" : label}
            </span>
          </NavLink>
        ))}
      </nav>
    </>
  );
}
