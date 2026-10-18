# RI140 related ordinary-signal startup defect

Root independently inspected the immutable RI138 owned_process.py Sink constructor
and complete run_child setup/finalization after QR reported the adjacent path.
Sink initializes safe state before its exclusive open, but run_child installs
record-only TERM/INT/HUP handlers only after creating and registering four sinks,
synchronizing the directory and acquiring the selector. The inherited parent
handler raises Refused during that startup interval. A signal after Sink's
successful open but before owner.sinks assignment can therefore leave a resource
outside the known-owner cleanup set. This is the same ordinary-signal acquisition
class as F01, at a second acquisition site, not an executed counterexample.

RI140 includes the minimal related startup-order repair within F01: establish
record-only ordinary-signal handling under the existing protected cleanup path
before acquiring startup resources; preserve and later refuse any recorded
signal, register acquired resources before subsequent fallible work, restore every
successfully changed handler on all ordinary tails, and keep the existing hard
watchdog behavior and incomplete hard-stop limitation explicit. The signal cannot
be silently discarded or converted to success, and no deadline/cap changes follow.

Include this actual changed function in the complete diff/correspondence and
focused prospective qualification design. A separate new launcher, scientific
target or general cleanup redesign is not assigned. Complete fresh nonauthor
review and root adjudication still precede any operational or fault execution.
RI138 remains immutable; the accepted RI139 operation is unrelated to this issue.
