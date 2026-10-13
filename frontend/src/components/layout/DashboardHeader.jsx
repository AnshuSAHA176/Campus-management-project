import { Search, Bell, CalendarDays, Clock } from "lucide-react";

export default function DashboardHeader() {
  return (
    <header
      className="sticky top-0 z-30 flex w-full min-w-0
      items-center gap-2 border-b border-[#242832]
      bg-[#080B11] px-3 py-3 sm:gap-3 sm:px-6"
    >
      {/* Search */}
      <div
        className="flex min-w-0 flex-1 items-center gap-2
        rounded-xl border border-[#252A35] bg-[#151A24]
        px-3 py-3 sm:gap-3 sm:px-4"
      >
        <Search size={20} className="shrink-0 text-slate-400" />

        <input
          type="search"
          aria-label="Search teachers, subjects or rooms"
          placeholder="Search teachers, subjects or rooms..."
          className="w-full min-w-0 bg-transparent text-sm
            text-white outline-none placeholder:text-slate-500
            sm:text-base"
        />
      </div>

      {/* Date: visible on tablets and larger screens */}
      <div
        className="hidden items-center gap-2 rounded-xl
        border border-[#252A35] px-3 py-3 text-sm
        text-slate-300 md:flex"
      >
        <CalendarDays size={17} className="shrink-0" />
        <span className="whitespace-nowrap">
          {new Date().toLocaleDateString("en-IN", {
            day: "2-digit",
            month: "short",
            year: "numeric",
          })}
        </span>
      </div>

      {/* Time: visible on larger screens */}
      <div
        className="hidden items-center gap-2 rounded-xl
        border border-[#252A35] px-3 py-3 text-sm
        text-slate-300 lg:flex"
      >
        <Clock size={17} className="shrink-0" />
        <span className="whitespace-nowrap">
          {new Date().toLocaleTimeString("en-IN", {
            hour: "2-digit",
            minute: "2-digit",
          })}
        </span>
      </div>

      {/* Notifications */}
      <button
        type="button"
        aria-label="Notifications"
        className="relative shrink-0 rounded-xl
          border border-[#252A35] p-3 text-slate-300
          transition-colors hover:text-[#FF642D]
          focus-visible:outline-none focus-visible:ring-2
          focus-visible:ring-[#FF642D]"
      >
        <Bell size={20} />

        {/* Optional unread notification badge */}
        <span
          className="absolute right-1 top-1 size-2
          rounded-full bg-[#FF642D]"
        />
      </button>
    </header>
  );
}
