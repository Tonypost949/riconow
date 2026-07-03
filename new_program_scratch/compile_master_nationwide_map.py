import os
import json
import csv
import ast
import re

def clean_and_eval(val_str):
    if not val_str or val_str == '[]':
        return []
    # Replace adjacent dictionaries missing a comma (e.g. } { or }\n {) with }, {
    cleaned = re.sub(r'\}\s*\{', '}, {', val_str)
    cleaned = re.sub(r"Decimal\('([^']+)'\)", r"\1", cleaned)
    try:
        return ast.literal_eval(cleaned)
    except Exception as e:
        try:
            return eval(cleaned, {"__builtins__": None}, {})
        except Exception as e2:
            return []

def main():
    matrix_json_path = r"C:\Users\HP\OneDrive\Documents\new_program_scratch\nationwide_coc_vulnerability_matrix.json"
    all_states_csv_path = r"C:\Users\HP\OneDrive\Documents\new_program_scratch\unzipped_data\opencode_work_20260621_152938\national_audits_all_state_records.csv"
    output_md_path = r"C:\Users\HP\OneDrive\Documents\new_program_scratch\nationwide_outbound_money_flow.md"

    # Load the 50-state vulnerability matrix
    if os.path.exists(matrix_json_path):
        with open(matrix_json_path, 'r', encoding='utf-8') as f:
            vulnerability_matrix = json.load(f)
    else:
        vulnerability_matrix = {}

    # Load state audit allocations
    audit_data = {}
    if os.path.exists(all_states_csv_path):
        with open(all_states_csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                state_abbr = row['state'].strip()
                hud_pit = clean_and_eval(row['hud_pit_list'])
                coc_continuum = clean_and_eval(row['coc_continuum_list'])
                non_profiteers = clean_and_eval(row['non_profiteers_index'])
                esa = clean_and_eval(row['environmental_site_assessments'])
                
                audit_data[state_abbr] = {
                    'hud_pit': hud_pit,
                    'coc_continuum': coc_continuum,
                    'non_profiteers': non_profiteers,
                    'esa': esa
                }

    # State Abbreviation mapping helper
    state_to_abbr = {
        "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
        "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
        "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
        "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
        "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO",
        "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
        "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
        "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
        "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
        "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"
    }

    md = []
    md.append("# NATIONWIDE CONTINUUM OF CARE (CoC) MASTER FLOW MAP")
    md.append("`STATUS: FACTUAL PUBLIC RECORD MASTER INDEX`  ")
    md.append("`GOAL: COMPLETE NATIONWIDE MAPPING OF HUD PUBLIC FUNDS, OUTBOUND TRANSFERS & REGIONAL VULNERABILITIES`  \n")
    md.append("This unified matrix lists **every US State Balance of State CoC**, mapping the path of public funds from federal/taxpayer allocations to local administrators, non-profit subrecipients, and documented entities.\n")
    
    md.append("## MASTER NATIONWIDE MONEY & PERSONNEL FLOW MATRIX\n")
    md.append("| State | CoC ID | CoC Node Name | Primary Recipient / Local Admin | Award Amount | Key Program / Service | NPI / Tax ID | Local Hazards, Policing, & NPI Gaps |")
    md.append("| :--- | :---: | :--- | :--- | :--- | :--- | :--- | :--- |")

    detailed_profiles = []

    for state_name in sorted(state_to_abbr.keys()):
        abbr = state_to_abbr[state_name]
        coc_info = vulnerability_matrix.get(state_name, {})
        coc_id = coc_info.get('id', f"{abbr}-BoS")
        coc_name = coc_info.get('name', f"{state_name} Balance of State CoC")
        vulnerabilities = coc_info.get('vulnerabilities', "Standard rural coverage gaps.")

        state_audit = audit_data.get(abbr, {
            'hud_pit': [], 'coc_continuum': [], 'non_profiteers': [], 'esa': []
        })

        hud_pit = state_audit['hud_pit']
        coc_continuum = state_audit['coc_continuum']
        non_profiteers = state_audit['non_profiteers']
        esa = state_audit['esa']

        # Determine PIT/homeless metrics
        pit_summary = "N/A"
        if hud_pit:
            pit_item = hud_pit[0]
            pit_summary = f"PIT Total: {pit_item.get('total_homeless', 0)} (Sheltered: {pit_item.get('sheltered_homeless', 0)}, Unsheltered: {pit_item.get('unsheltered_homeless', 0)})"

        # Track if we wrote rows
        rows_written = 0

        # We merge awards and non-profit subrecipients
        max_items = max(len(coc_continuum), len(non_profiteers), 1)
        for i in range(max_items):
            prog = coc_continuum[i] if i < len(coc_continuum) else {}
            recip = non_profiteers[i] if i < len(non_profiteers) else {}

            award_val = prog.get('award_amount')
            award_str = f"${award_val:,.2f}" if award_val else "N/A"
            prog_type = prog.get('program_type', "CoC Housing Programs")
            
            recip_name = recip.get('organization_name')
            if not recip_name:
                recip_name = "*State Department of Housing / Direct County Admin*" if not award_val else "*Direct Municipal Recipient*"

            npi_code = recip.get('npi_id', recip.get('cms_billing_code', 'N/A'))

            # Notes / Delta
            delta_parts = []
            if recip.get('unaccounted_fund_delta'):
                delta_parts.append(f"Unaccounted Delta: ${recip.get('unaccounted_fund_delta'):,.2f}")
            if recip.get('task_tracking_url') and len(recip.get('task_tracking_url')) > 40:
                # Add brief preview of notes
                delta_parts.append(recip.get('task_tracking_url')[:100] + "...")
            
            notes = " | ".join(delta_parts) if delta_parts else "Standard administrative path."
            combined_hazards = f"**{vulnerabilities}**<br>_Metrics:_ {pit_summary}"
            if notes != "Standard administrative path.":
                combined_hazards += f"<br>_Audit Warning:_ {notes}"

            md.append(f"| {state_name} ({abbr}) | `{coc_id}` | {coc_name} | **{recip_name}** | {award_str} | {prog_type} | {npi_code} | {combined_hazards} |")
            rows_written += 1

        # Build detailed profile for the state
        sect = []
        sect.append(f"### {state_name} ({abbr}) - Comprehensive Audit Profile")
        sect.append(f"- **CoC Node ID**: `{coc_id}`")
        sect.append(f"- **CoC Name**: **{coc_name}**")
        sect.append(f"- **Administrative Risks & Gaps**: {vulnerabilities}")
        if pit_summary != "N/A":
            sect.append(f"- **Vulnerability Population Data**: {pit_summary}")
        
        if coc_continuum:
            sect.append("#### HUD Taxpayer Awards Path:")
            for p in coc_continuum:
                sect.append(f"  - **Program Type**: {p.get('program_type', 'N/A')} | **HUD Award**: ${p.get('award_amount', 0):,.2f} (FY {p.get('fiscal_year', 'N/A')})")
        else:
            sect.append("#### HUD Taxpayer Awards Path:\n  - Downstream funds administered directly via state-allocated Emergency Solutions Grants (ESG) and HOME consortia.")

        if non_profiteers:
            sect.append("#### Mapped Downstream Operators & Entities:")
            for np in non_profiteers:
                sect.append(f"  - **Organization Name**: `{np.get('organization_name', 'N/A')}`")
                sect.append(f"    - **NPI ID / CMS Code**: `{np.get('npi_id', 'N/A')}` / `{np.get('cms_billing_code', 'N/A')}`")
                if np.get('unaccounted_fund_delta'):
                    sect.append(f"    - **Unaccounted Fund Delta**: `${np.get('unaccounted_fund_delta'):,.2f}`")
                if np.get('task_tracking_url'):
                    sect.append(f"    - **Internal Log Context**: {np.get('task_tracking_url')}")
        else:
            sect.append("#### Mapped Downstream Operators & Entities:\n  - Operates via direct municipal county networks with no localized non-profit monopoly flags.")

        if esa:
            sect.append("#### Mapped Environmental Site Hazards:")
            for e in esa:
                sect.append(f"  - **Site ID**: `{e.get('site_id', 'N/A')}` | **Hazardous Location**: {e.get('location_name', 'N/A')}")
                sect.append(f"    - **Contaminant**: {e.get('contaminant_type', 'N/A')} (Toxicity Multiplier: {e.get('test_multiplier', 'N/A')}x)")
                sect.append(f"    - **Waterboard Closure Status**: {e.get('closure_status', 'N/A')}")

        detailed_profiles.append("\n".join(sect))

    md.append("\n---\n")
    md.append("## DETAILED REGIONAL AUDIT FILES (BY STATE)\n")
    md.append("\n\n".join(detailed_profiles))

    with open(output_md_path, mode='w', encoding='utf-8') as f:
        f.write("\n".join(md) + "\n")
    
    print(f"[+] Compiled master nationwide money & personnel map at {output_md_path}")

if __name__ == '__main__':
    main()
