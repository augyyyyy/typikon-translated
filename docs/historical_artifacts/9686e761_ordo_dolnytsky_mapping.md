# Liturgical Hierarchy & Coverage Map

As we continue to verify and extract the draft booklets for the parish, it is critical to clearly establish the jurisdictional boundaries between our two master reference texts. 

The **Roman 1996 Ordo Celebrationis** is the supreme law, but its scope is intentionally limited. The **Dolnytsky Typikon** acts as the comprehensive customary that fills in all the gaps where the Ordo is silent.

Here is the exact mapping of what each text covers explicitly:

## 1. Ordo Celebrationis (Supreme Law)
The *Ordo Celebrationis* (published in Rome in 1944, translated 1996) was issued by the Sacred Congregation for the Eastern Churches to establish the authentic "Ruthenian Recension" mechanics. It governs the physical actions, vesture, and exact wording for the primary public worship services.

**Explicit Scope:**
- **Vespers (With and Without Vigil):** It outlines the complete structure, including provisions for celebration with one deacon, two deacons, or no deacon, as well as concelebrating priests.
- **Orthros (Matins):** It covers Matins *specifically* for Sundays and Feast Days. 
- **Divine Liturgies:** 
  - Liturgy of St. John Chrysostom
  - Liturgy of St. Basil the Great
  - Liturgy of the Presanctified Gifts
- **General Rules:** Extensive rules on bows, censing, and the sanctuary layout.

**Notable Omissions:**
The Ordo does *not* cover Daily Matins, Small Matins, Small Vespers, the Minor Hours (1st, 3rd, 6th, 9th), Compline, the Midnight Office, the Typika service, or the granular calendar rules for the Menaion and Triodion.

---

## 2. Dolnytsky Typikon (Subordinate Customary)
The Dolnytsky Typikon (based on the Lviv Synod) is the comprehensive rulebook. It is subordinate to the Ordo, meaning *the Typikon applies only as far as the Ordo is silent or does not explicitly contradict it.*

**Explicit Scope:**
- **The Minor Hours:** The structure and mechanics for Compline (Great and Small), Midnight Office (Daily, Saturday, Sunday), all the Little Hours (1st, 3rd, 6th, 9th), and the Typika.
- **Daily & Small Services:** It provides the rules for Daily Matins, Small Matins, and Small Vespers. (This is where Dolnytsky's strict rule against deacons at Daily Vespers comes from, though it is superseded by the Ordo's broader Vespers allowances).
- **The Calendar System (The "When" & "What"):**
  - **Menaion (Fixed Cycle):** Detailed rubrics on how to combine feasts (e.g., when a Polyeleos saint falls on a Sunday, or when the Annunciation falls on Good Friday).
  - **Triodion & Pentecostarion (Moveable Cycle):** The specific structural changes required during Great Lent, Holy Week, and the Paschal season.
- **Temple Architecture:** Specific directives on vestment colors, church vessels, and altar linens.

---

### Conclusion for Booklet Automation
When auditing or generating a booklet, our AI pipeline must process queries through this hierarchy:
1. **How is a major service performed?** $\rightarrow$ Check the *Ordo Celebrationis* first.
2. **How is a minor service performed?** $\rightarrow$ Check the *Dolnytsky Typikon*.
3. **What specific hymns are sung today?** $\rightarrow$ Check the *Dolnytsky Typikon* (Menaion/Triodion sections). 
4. **What terminology do we use?** $\rightarrow$ Check the Parish Lexical Matrix (Stamford English vocabulary).
