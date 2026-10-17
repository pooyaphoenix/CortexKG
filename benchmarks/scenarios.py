"""
Dataset for evaluating CortexKG's graph-based reasoning against raw LLM context.
These scenarios test multi-path graph traversal, distractor resistance, and temporal state resolution.
"""

BENCHMARK_SUITE = [
    
    {
        "id": "scenario_4_temporal_state_override",
        "name": "Temporal Policy Override & State Resolution",
        "documents": [
            "Protocol Directive 12 states that any server hosting 'Level A' data must use Quantum-Shield encryption.",
            "In Q1, Server Node X-99 was assigned to host the 'Level A' user database.",
            "In Q2, Server Node X-99 experienced a critical failure, and its database was permanently migrated to Backup Node Z-4.",
            "In Q3, a new security mandate superseded Directive 12: Level A data now strictly requires 'Aegis-Vault' encryption, deprecating Quantum-Shield.",
            "In Q4, Backup Node Z-4 received a compliance audit."
        ],
        "question": "During its Q4 audit, what specific encryption method must Backup Node Z-4 use, and what data classification triggers this requirement?",
        "ground_truth_answer": "Aegis-Vault, Level A",
        "key_entities": ["aegis-vault", "level a"]
    },
    
    {
        "id": "scenario_5_persian_ownership_trace",
        "name": "Persian Multi-Hop Corporate Ownership & Distractor Resistance",
        "documents": [
            "شرکت توسعه آلفا در سال ۱۴۰۱ تاسیس شد و در زمینه هوش مصنوعی فعالیت می‌کند.",
            "مالکیت کامل و ۱۰۰ درصدی شرکت توسعه آلفا در اختیار هلدینگ فناوری مهر است.",
            "هلدینگ فناوری مهر در ماه گذشته، ۷۰ درصد از سهام مدیریتی خود را به گروه سرمایه‌گذاری نوین واگذار کرد.",
            "مدیرعامل گروه سرمایه‌گذاری نوین، آقای سینا تهرانی است.",
            "ردگم‌کنی ۱: شرکت پردازش بتا نیز توسط آقای سینا تهرانی تاسیس شده است اما هیچ ارتباطی با هلدینگ فناوری مهر ندارد.",
            "ردگم‌کنی ۲: هلدینگ پارس مالک شرکت دلتا است و در زمینه ساخت و ساز فعالیت می‌کند.",
            "ردگم‌کنی ۳: شرکت توسعه آلفا قبلا با شرکت پردازش بتا همکاری موقتی داشته است."
        ],
        "question": "بر اساس آخرین تغییرات سهام، شرکت توسعه آلفا به طور غیرمستقیم تحت مدیریت چه کسی قرار دارد و نام هلدینگ واسط چیست؟",
        "ground_truth_answer": "سینا تهرانی, هلدینگ فناوری مهر",
        "key_entities": ["سینا تهرانی", "هلدینگ فناوری مهر", "فناوری مهر"]
    }
]