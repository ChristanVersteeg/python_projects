import win32com.client as win32
from win32com.client import gencache

# -------------------------------------------------------------------
# Manual constants (values from the Office object model)
# -------------------------------------------------------------------
PP_LAYOUT_BLANK = 12                 # ppLayoutBlank
MSO_TEXT_ORIENTATION_HORIZONTAL = 1  # msoTextOrientationHorizontal

MSO_ANIM_EFFECT_CUSTOM = 0           # msoAnimEffectCustom
MSO_ANIM_EFFECT_APPEAR = 1           # msoAnimEffectAppear

MSO_ANIM_TRIGGER_ON_PAGE_CLICK = 1   # msoAnimTriggerOnPageClick
MSO_ANIM_TRIGGER_WITH_PREVIOUS = 2   # msoAnimTriggerWithPrevious

MSO_ANIM_TYPE_MOTION = 1             # msoAnimTypeMotion

# -------------------------------------------------------------------
# Start PowerPoint
# -------------------------------------------------------------------
ppt = gencache.EnsureDispatch("PowerPoint.Application")
ppt.Visible = True

pres = ppt.Presentations.Add()
slide = pres.Slides.Add(1, PP_LAYOUT_BLANK)

# -------------------------------------------------------------------
# Your text paragraphs
# -------------------------------------------------------------------
paragraphs = [
    "wel eens denkt dat sommige beveiligingsmaatregelen “onnodig veel gedoe” zijn.",
    "wel eens op “Akkoord” hebt geklikt zonder de privacyvoorwaarden te lezen.",
    "weleens een verdachte e-mail hebt geopend.",
    "je gegevens ooit hebt ingevuld bij een winactie.",
    "updates uitstelt omdat je ‘geen tijd’ hebt.",
    "iets online hebt besteld en nooit ontvangen.",
    "denkt dat cybersecurity een taak voor de IT-afdeling is en niet voor jou.",
    "wel eens vertrouwelijke documenten op je bureau hebt laten liggen.",
    "jouw scherm niet altijd vergrendelt wanneer je even wegloopt.",
    "toegang hebt tot meer systemen of gegevens dan je eigenlijk gebruikt.",
    "wel eens werkbestanden naar je privé-mail hebt gestuurd.",
    "een niet verplichte security e-learning overslaat.",
    "wel eens denkt dat sommige beveiligingsmaatregelen “onnodig veel gedoe” zijn.",
    "een keer iemand op het werk mee naar binnen liep die je niet goed kende.",
    "een datalek niet zou melden als het niet ‘erg genoeg’ is.",
    "niet precies weet welke richtlijnen voor AI de organisatie hanteert.",
    "denkt dat AI een taak beter kan dan een mens.",
    "wel eens AI betrouwbaar vond ‘omdat het zo zelfverzekerd klinkt’.",
    "AI-gegenereerde informatie hebt gebruikt zonder de bron te controleren.",
    "wel eens privé AI-tools hebt gebruikt voor werkdocumenten.",
    "AI hebt gebruikt terwijl je twijfelde of de dataset wel representatief was.",
    "AI gebruikt voor meer productiviteit, maar niet weet hoe je data wordt opgeslagen."
]

# -------------------------------------------------------------------
# Lay out each paragraph as its own text box
# -------------------------------------------------------------------
start_left = 80
start_top = 150
line_height = 35

shapes = []

for i, text in enumerate(paragraphs):
    shp = slide.Shapes.AddTextbox(
        Orientation=MSO_TEXT_ORIENTATION_HORIZONTAL,
        Left=start_left,
        Top=start_top + i * line_height,
        Width=800,
        Height=30
    )
    tr = shp.TextFrame.TextRange
    tr.Text = text
    tr.Font.Size = 20
    shapes.append(shp)

# -------------------------------------------------------------------
# Build animations
# -------------------------------------------------------------------
seq = slide.TimeLine.MainSequence
slide_height = pres.PageSetup.SlideHeight

# Remember original tops so we can compute motion distances
initial_tops = [sh.Top for sh in shapes]
top_slot = initial_tops[0]  # the position of the first line

# 1) First line: simple appear on click
first_effect = seq.AddEffect(
    Shape=shapes[0],
    effectId=MSO_ANIM_EFFECT_APPEAR,
    trigger=MSO_ANIM_TRIGGER_ON_PAGE_CLICK
)
first_effect.Timing.Duration = 0.01

# 2) For every subsequent line:
#    - click -> new line appears
#    - previous line disappears (exit)
#    - new line moves up into top_slot (motion path)
for i in range(1, len(shapes)):
    prev_shape = shapes[i - 1]
    shape = shapes[i]

    # Appear current line on next click
    appear = seq.AddEffect(
        Shape=shape,
        effectId=MSO_ANIM_EFFECT_APPEAR,
        trigger=MSO_ANIM_TRIGGER_ON_PAGE_CLICK
    )
    appear.Timing.Duration = 0.01

    # Previous line disappears WITH that click (EXIT animation)
    disappear_prev = seq.AddEffect(
        Shape=prev_shape,
        effectId=MSO_ANIM_EFFECT_APPEAR,     # base effect type
        trigger=MSO_ANIM_TRIGGER_WITH_PREVIOUS
    )
    disappear_prev.Exit = True              # <-- mark as exit = Disappear
    disappear_prev.Timing.Duration = 0.01

    # Custom motion path for current line, WITH the same click
    move_effect = seq.AddEffect(
        Shape=shape,
        effectId=MSO_ANIM_EFFECT_CUSTOM,
        trigger=MSO_ANIM_TRIGGER_WITH_PREVIOUS
    )

    beh = move_effect.Behaviors.Add(MSO_ANIM_TYPE_MOTION)
    motion = beh.MotionEffect

    # Move from its original row to the top row (where the first/previous was)
    delta_points = top_slot - initial_tops[i]   # negative => move up

    # ByY is in percent of slide height (100 = full slide height)
    motion.ByX = 0
    motion.ByY = (delta_points / slide_height) * 100.0

    move_effect.Timing.Duration = 0.4

# -------------------------------------------------------------------
# Save the file (change path if you like)
# -------------------------------------------------------------------
output_path = r"C:\Users\Public\cybersecurity_paragraphs_with_exit.pptx"
pres.SaveAs(output_path)

print(f"Done. Saved to: {output_path}")
print("Open it and check Animations -> Animation Pane (you should see red Exit icons now).")
