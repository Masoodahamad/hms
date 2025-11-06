import argparse, requests, json, sys
BASE = "http://127.0.0.1:5000/api"

def post(path, data):
    r = requests.post(f"{BASE}{path}", json=data, timeout=10)
    print(r.status_code, r.json())

def get(path):
    r = requests.get(f"{BASE}{path}", timeout=10)
    print(r.status_code, json.dumps(r.json(), indent=2))

def main(argv=None):
    ap = argparse.ArgumentParser(description="Minimal CLI for HMS API")
    sub = ap.add_subparsers(dest="cmd")

    p_new = sub.add_parser("new-patient")
    p_new.add_argument("--name", required=True)
    p_new.add_argument("--dob", required=True, help="YYYY-MM-DD")
    p_new.add_argument("--email")
    p_new.add_argument("--gender")
    p_new.add_argument("--phone")
    p_new.add_argument("--address")

    sub.add_parser("list-patients")

    d_new = sub.add_parser("new-doctor")
    d_new.add_argument("--name", required=True)
    d_new.add_argument("--specialty")

    a_new = sub.add_parser("new-appt")
    a_new.add_argument("--patient_id", type=int, required=True)
    a_new.add_argument("--doctor_id", type=int, required=True)
    a_new.add_argument("--visit_time", required=True, help="YYYY-MM-DDTHH:MM")

    args = ap.parse_args(argv)
    if args.cmd == "new-patient":
        post("/patients", vars(args))
    elif args.cmd == "list-patients":
        get("/patients")
    elif args.cmd == "new-doctor":
        post("/doctors", vars(args))
    elif args.cmd == "new-appt":
        post("/appointments", vars(args))
    else:
        ap.print_help()

if __name__ == "__main__":
    main()
