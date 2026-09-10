# 05 — Information Architecture

## Form factors

| Role | Target | Layout | Rationale |
|---|---|---|---|
| Customer | Phone, ~390pt | Single column, **bottom tab bar** | Rendered in a phone frame in every prototype screenshot |
| Valet | Tablet, landscape | **4-column kanban board**, full-bleed | Kiosk at the valet stand; stays signed in |
| Garage Manager | Desktop | Fixed **left sidebar** + content | Grouped sidebar with section headings |
| Office Admin | Desktop | Fixed **left sidebar** + content | Same chrome as Manager, different items |

Build **one responsive web application**. The valet board and the admin consoles
collapse acceptably to narrower widths; the customer shell is the only view with a
genuinely distinct navigation pattern, and it is the one that ships as an installable
PWA behind the QR code.

## Route map *(proposed — the prototype is a single-page demo without visible routes)*

```
/                                   Landing (logo, Sign In, Create Account, QR)
/sign-in                            Sign in
/sign-up                            Enrollment (access code → identifier → profile)
/forgot-password

── Customer (mobile shell) ─────────────────────────────────────────
/app                                Home — vehicles + live request status
/app/requests/:id                   Request status — progress + cancel
/app/schedule                       Schedule a pickup + upcoming list
/app/vehicles                       My vehicles
/app/vehicles/new                   Add a vehicle
/app/notifications                  Notification list  (bell icon)

── Valet (tablet board) ────────────────────────────────────────────
/valet                              Queue board (4 columns)
/valet/requests/:id                 Request detail  (modal over the board)
/valet/directory                    Valet menu — customers | vehicles | pickups (modal)

── Garage Manager (desktop) ────────────────────────────────────────
/manager                            Dashboard
/manager/approvals                  Pending Approvals
/manager/customers                  Customers & Vehicles
/manager/valet-accounts             Valet Account
/manager/history                    Request History
/manager/settings                   Settings (chime)

── Office Admin (desktop) ──────────────────────────────────────────
/admin                              Office Console
/admin/users                        Users (staff | customers)
/admin/locations                    Locations
/admin/activity                     Activity History
/admin/settings                     Settings & Operational Policies
```

Detail views on the valet board are **modals over the board**, not full pages — the
queue stays visible behind them. Give them addressable URLs anyway so a page refresh
on a tablet restores context.

## Navigation

### Customer — bottom tab bar

```
┌──────────────────────────────────────────┐
│  [P logo]        🔔   👁 Viewing as ▾    │  ← header
├──────────────────────────────────────────┤
│                                          │
│               content                    │
│                                          │
├──────────────────────────────────────────┤
│    ⊞ Home     📅 Schedule    🚗 Vehicle   │  ← 3 tabs, active = brand red
└──────────────────────────────────────────┘
```

Three tabs only: **Home · Schedule · Vehicle**. Active tab renders icon and label in
brand red; inactive in slate. The `Viewing as` control is a prototype affordance and
must not ship *(see doc 02)*.

### Valet — board chrome

```
┌──────────────────────────────────────────────────────────────────────┐
│  [P logo]              📍 Wacker Drive Garage   👁 Viewing as ▾  ⋮   │
├──────────────────────────────────────────────────────────────────────┤
│  Valet Queue                                                          │
├──────────────────────────────────────────────────────────────────────┤
│  🔔 1 request awaiting acceptance — Accept to stop the alert.         │  ← conditional
├──────────────────────────────────────────────────────────────────────┤
│  INCOMING 1  │ ACTIVE QUEUE 3 │ TOMORROW'S 1 │ FUTURE PICKUPS 1      │
└──────────────────────────────────────────────────────────────────────┘
```

No sidebar. The valet's entire application is one board plus a **⋮ kebab** that opens
the read-only Valet menu. This is correct for a kiosk: one screen, no navigation to get
lost in, everything reachable in one tap.

### Manager sidebar

```
OVERVIEW
  ⊞  Dashboard
OPERATIONS
  ☑  Pending Approvals
  👥 Customers & Vehicles
ADMINISTRATION
  👤 Valet Account
  🕘 Request History
  ⚙  Settings
```

### Admin sidebar

```
OVERVIEW
  ⊞  Console
ADMINISTRATION
  👥 Users
  📍 Locations
  📈 Activity History
  ⚙  Settings
```

Both sidebars: logo top-left, uppercase slate section labels, active item as a
red-tinted pill with red icon and label. Section grouping is meaningful — *Operations*
is day-to-day work, *Administration* is configuration — and worth keeping as the app
grows.

### Header scope controls

| Role | Location control | Behavior |
|---|---|---|
| Valet | `📍 Wacker Drive Garage` | **Static label.** One location, not switchable |
| Manager | `📍 Wacker Drive Garage` | Static label in the prototype, but managers can hold multiple locations — **must become a picker** *(inferred requirement)* |
| Admin | `[Wacker Drive Garage ▾]` | **Dropdown.** Scopes Users, Activity, Settings |

The Manager case is a genuine prototype gap: Hector Flores manages State Street Garage
*and* River North Condos, and the prototype gives him no way to switch. Build the
picker.

## Screen inventory

| # | Screen | Role | Reference |
|---|---|---|---|
| 1 | Landing / QR | Public | `screens/customer/00-landing-qr.png` |
| 2 | Sign in | Public | `screens/customer/01-sign-in.png` |
| 3 | Home | Customer | `screens/customer/02-home.png` |
| 4 | Request status | Customer | `screens/customer/03-request-status.png` |
| 5 | Schedule a pickup | Customer | `screens/customer/04-schedule-pickup.png` |
| 6 | My vehicles | Customer | `screens/customer/05-my-vehicles.png` |
| 7 | Add a vehicle | Customer | `screens/customer/06-add-vehicle.png` |
| 8 | Queue board | Valet | `screens/valet/01-queue.png` |
| 9 | Request detail | Valet | `screens/valet/02-request-detail.png` |
| 10 | Valet menu | Valet | `screens/valet/03-valet-menu.png` |
| 11 | Dashboard | Manager | `screens/manager/01-dashboard.png` |
| 12 | Pending Approvals | Manager | `screens/manager/02-pending-approvals.png` |
| 13 | Customers & Vehicles | Manager | `screens/manager/03-customers-vehicles.png` |
| 14 | Valet Account | Manager | `screens/manager/04-valet-account.png` |
| 15 | Request History | Manager | `screens/manager/05-request-history.png` |
| 16 | Settings | Manager | `screens/manager/06-settings.png` |
| 17 | Office Console | Admin | `screens/admin/01-console.png` |
| 18 | Users | Admin | `screens/admin/02-users.png` |
| 19 | Locations | Admin | `screens/admin/03-locations-add.png`, `04-locations-list.png` |
| 20 | Activity History | Admin | `screens/admin/05-activity-history.png` |
| 21 | Settings & Policies | Admin | `screens/admin/06-settings-policies.png` |

**Screens the product needs that the prototype does not show** — scope these
explicitly rather than discovering them in sprint 3:

- Sign-up / enrollment flow (access code → identifier → profile → first vehicle)
- Forgot password / reset password
- Notification list behind the customer's bell icon
- Customer profile & account settings (change phone, email, password)
- Empty states for a brand-new customer with zero vehicles
- Error, offline, and connection-lost states — **critical for the valet tablet**
- Admin → Users → **Customers** tab (the tab exists; only *Staff* is shown)
- Approval **Review** detail view (the button exists; the destination is not shown)
- Confirmation dialogs for destructive actions (Suspend, Disable, Regenerate, Reject)
