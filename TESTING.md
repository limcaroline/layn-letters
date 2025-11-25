# Layn Letters – Testing

---

**Contents**
- [Layn Letters – Testing](#layn-letters--testing)
  - [Responsiveness](#responsiveness)
    - [Mobile Screenshots](#mobile-screenshots)
    - [Tablet Screenshots](#tablet-screenshots)
    - [Desktop Screenshots](#desktop-screenshots)
  - [Validations](#validations)
    - [W3C Validator](#w3c-validator)
    - [JSHint](#jshint)
    - [Python Linter](#python-linter)
  - [Lighthouse](#lighthouse)
  - [Wave Webaim](#wave-webaim)
  - [Browser Compatibility](#browser-compatibility)
  - [Full Testing](#full-testing)
    - [Navigation](#navigation)
    - [Reviews](#reviews)
    - [Stories](#stories)
    - [Budgets](#budgets)
    - [Authentication](#authentication)
  - [Bugs](#bugs)
    - [Solved Bugs](#solved-bugs)
      - [Detailed Debug Notes](#detailed-debug-notes)
    - [Known Bugs](#known-bugs)

---

## Responsiveness

Layn Letters was tested across a range of viewport sizes using Chrome DevTools device toolbar to ensure a consistent experience on mobile, tablet and desktop.

### Mobile Screenshots

- Home

  ![Home – Mobile](resources/testing/responsiveness/mobile-home.png)

- Reviews

  ![Reviews – Mobile](resources/testing/responsiveness/mobile-reviews.png)

- Stories

  ![Stories – Mobile](resources/testing/responsiveness/mobile-stories.png)

- Budgets

  ![Budgets – Mobile](resources/testing/responsiveness/mobile-budgets.png)

### Tablet Screenshots

- Home

  ![Home – Tablet](resources/testing/responsiveness/tablet-home.png)

- Reviews

  ![Reviews – Tablet](resources/testing/responsiveness/tablet-reviews.png)

- Stories

  ![Stories – Tablet](resources/testing/responsiveness/tablet-stories.png)

- Budgets

  ![Budgets – Tablet](resources/testing/responsiveness/tablet-budgets.png)

### Desktop Screenshots

- Home

  ![Home – Desktop](resources/testing/responsiveness/desktop-home.png)

- Reviews

  ![Reviews – Desktop](resources/testing/responsiveness/desktop-reviews.png)

- Stories

  ![Stories – Desktop](resources/testing/responsiveness/desktop-stories.png)

- Budgets

  ![Budgets – Desktop](resources/testing/responsiveness/desktop-budgets.png)

---

## Validations

### W3C Validator

All top-level rendered templates were checked using:

- W3C HTML Validator: https://validator.w3.org/
- W3C CSS Validator: https://jigsaw.w3.org/css-validator/

Rendered HTML (via “View Source” in the browser) was pasted into the validator to avoid template-tag related false positives.

Examples:

- Initial HTML validation results showing inline `<style>` in templates.

  ![HTML validation – before fixes](resources/testing/validations/html-before.png)

- Footer template with inline styling identified.

  ![Footer template had inline style](resources/testing/validations/footer-before.png)

- Footer styles moved to the main stylesheet and revalidated.

  ![Footer CSS moved to stylesheet](resources/testing/validations/footer-after.png)

- Final HTML validation pass.

  ![HTML validation – after fixes](resources/testing/validations/html-after.png)

- CSS check returned no errors.

  ![CSS validation – no errors](resources/testing/validations/css-ok.png)

Note: Django template tags were rendered in the browser before validation.

### JSHint

JavaScript was validated with https://jshint.com/.

Key files checked included:

- Story voting script (AJAX `fetch` for story score updates).
- Budget total calculation script.
- Miscellaneous UI helpers.

Examples:

- JSHint flagged a compact `if`/`return` expression without braces.

  ![JSHint error](resources/testing/validations/jshint-before.png)

- The offending logic was rewritten to use explicit braces and clearer control flow, removing warnings.

  ![JSHint fixed](resources/testing/validations/jshint-after.png)

### Python Linter

Python code was validated using the Code Institute Python Linter (flake8-equivalent) across apps such as `reviews`, `stories`, `budgets` and `core`.

Example:

- No errors reported after minor formatting adjustments (line length, spacing, imports).

  ![Python linter – no errors](resources/testing/validations/python-linter-ok.png)

---

## Lighthouse

Lighthouse audits (Performance, Accessibility, Best Practices, SEO) were run from Chrome DevTools on key pages:

- Home
- Reviews list and detail
- Story list and detail
- Budget list and budget edit

Example report:

![Lighthouse testing results](resources/testing/lighthouse/lighthouse.png)

Where possible, minor issues such as missing `alt` attributes and low-contrast text were corrected to improve scores.

---

## Wave Webaim

Accessibility was checked using the WAVE browser extension: https://wave.webaim.org/

Results, among others:

- No critical accessibility errors on content pages.
- Color contrast checks passed after minor design adjustments.

![WAVE results](resources/testing/wave/webaim.png)

---

## Browser Compatibility

Tested on latest stable versions:

- Chrome (desktop)
- Safari (macOS)
- Firefox (desktop)
- Chrome (Android)

Examples:

- Safari screenshots:

  ![Safari 1](resources/testing/browsers/safari-1.png)  
  ![Safari 2](resources/testing/browsers/safari-2.png)  
  ![Safari 3](resources/testing/browsers/safari-3.png)  
  ![Safari 4](resources/testing/browsers/safari-4.png)

All core flows (navigation, authentication, reviews, stories, budgets) behaved consistently across tested browsers.

---

## Full Testing

All tests were performed both on the local development server (`http://127.0.0.1:8000`) and on the deployed build (where applicable).

### Navigation

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
|--------|------------------|-------------------|--------|-----------|
| Brand / Home link | Navigates to home page. | Clicked brand and Home from various pages. | Home loaded correctly. | Pass |
| Reviews link | Navigates to reviews list. | Clicked Reviews in navbar. | Reviews list shown. | Pass |
| Stories link | Navigates to stories list. | Clicked Stories in navbar. | Stories list shown. | Pass |
| Budgets link | Navigates to budgets list or create view. | Clicked Budgets. | Budget page displayed. | Pass |
| Login / Signup | Navigates to authentication pages. | Clicked Login / Signup as anonymous user. | Allauth pages displayed. | Pass |
| Logout | Logs user out and redirects to home. | Clicked Logout as logged-in user. | User logged out successfully. | Pass |

### Reviews

**Review List / Detail**

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
|--------|------------------|-------------------|--------|-----------|
| Review list pagination | Shows 10 reviews per page. | Added >10 reviews, navigated pages. | Pagination working. | Pass |
| Filter by place | Filters reviews by place name. | Used `?place=` querystring. | Only matching reviews shown. | Pass |
| Review detail | Shows place, rating, body, author, visited date. | Opened several reviews. | All fields rendered as expected. | Pass |
| Place average rating | Shows average rating per place. | Added multiple reviews for one place, checked detail page. | Calculated correctly with `Avg("rating")`. | Pass |

**Review Comments and Voting**

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
|--------|------------------|-------------------|--------|-----------|
| Add comment (authenticated) | Saves new comment and shows on review. | Posted valid comment while logged in. | Comment saved and listed. | Pass |
| Redirect to login (anonymous) | Anonymous users are redirected. | Tried posting comment while logged out. | Redirected to login. | Pass |
| Comment score | Shows sum of all votes for a comment. | Upvoted and downvoted a comment from different users. | Score reflects sum of `value` in `ReviewCommentVote`. | Pass |
| Vote up/down | Each user can upvote or downvote. | Clicked + and - on the same comment. | Vote stored/updated correctly. | Pass |
| Vote toggle behaviour | Switching from + to - and vice versa adjusts score by 1 per click. | Repeatedly clicked + and - on a single comment as the same user. | Behaviour matched tri-state logic (-1, 0, +1) and score changed predictably. | Pass |
| Comment edit | Authors can edit their own comments. | Clicked Edit on own comment. | Change saved and updated. | Pass |
| Comment delete | Authors or site owner can delete comments. | Deleted comment as author and as site owner. | Comment removed, redirect back to review. | Pass |

### Stories

**Story List / Detail**

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
|--------|------------------|-------------------|--------|-----------|
| Published filter | Only `status="published"` stories appear in list. | Created draft and published stories, loaded list. | Only published stories listed. | Pass |
| Story detail | Shows title, author, date, category, content and optional cover image. | Opened multiple stories. | All fields displayed correctly. | Pass |
| Slug routing | Stories accessible by slug in URL. | Navigated via story list links. | Correct story loaded by slug. | Pass |

**Story Voting (Score)**

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
|--------|------------------|-------------------|--------|-----------|
| Initial score | Aggregates story `Vote.value` before interaction. | Loaded story with existing votes. | Score from context matched DB aggregate. | Pass |
| Upvote story | Clicking + sends POST to `VoteToggle` and updates score. | Clicked + as logged-in user. | JSON response returned and DOM updated via JS. | Pass |
| Downvote story | Clicking - updates score accordingly. | Clicked - after upvote. | Score adjusted in line with backend aggregate. | Pass |
| Single vote per user | Each user only has one row in `Vote`. | Checked DB and behaviour when clicking multiple times. | `unique_together` enforced (no duplicates). | Pass |
| Anonymous voting blocked | Anonymous users cannot vote. | Clicked + when logged out. | Redirected to login or no effect, depending on configuration. | Pass |

**Story Comments and Scores**

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
|--------|------------------|-------------------|--------|-----------|
| Add top-level comment | Saves comment with `parent=None`. | Submitted comment form on story detail. | Comment displayed in list. | Pass |
| Comment ordering | Newer comments appear first. | Added multiple comments. | Ordered by `-created`. | Pass |
| Comment score display | Score uses `annotate(score=Sum("votes__value"))`. | Added votes to comments, refreshed page. | Comment scores displayed correctly. | Pass |
| Comment vote API | `CommentVoteToggle` updates or creates `CommentVote`. | Posted up/down votes. | Values stored correctly in DB. | Pass |

### Budgets

**Budget Form and Items**

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
|--------|------------------|-------------------|--------|-----------|
| Create budget | Saves budget title, currency and notes. | Submitted valid form. | Budget created and visible in list. | Pass |
| Formset items | Each item includes day, name, category, quantity, unit cost, notes. | Added multiple items. | All fields saved. | Pass |
| Delete existing item | Delete checkbox removes item on save. | Ticked Delete on one row. | Item removed after submit. | Pass |

**JavaScript Total Calculation**

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
|--------|------------------|-------------------|--------|-----------|
| Total updates on change | Changing quantity or unit cost updates Total display. | Changed fields in several rows with different values. | Total recalculated correctly. | Pass |
| Decimal comma handling | Inputs using comma as decimal are parsed correctly. | Entered values like `1,50` and `2,75` for qty and price. | JS converted and summed correctly. | Pass |
| Per-row selection | Only numeric inputs in budget rows are included in total. | Mixed text and number inputs in table. | JS targeted `.js-qty` and `.js-unit` classes only. | Pass |
| Initial total on page load | Existing budget items are summed when page opens. | Edited existing budget with pre-filled items. | Total display showed correct sum before changes. | Pass |

### Authentication

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
|--------|------------------|-------------------|--------|-----------|
| Signup | New user can register an account. | Submitted signup form. | User created and logged in. | Pass |
| Login | Existing user can log in. | Logged in with valid credentials. | Login succeeded. | Pass |
| Logout | User is logged out and redirected. | Clicked Logout link. | Session cleared. | Pass |
| Auth-only views | Protected views require login. | Visited protected URLs logged out. | Redirected to login. | Pass |
| Owner-only review/story actions | Only site owner or author can edit/delete. | Attempted edit/delete as different users. | Access restricted correctly. | Pass |

---

## Bugs

### Solved Bugs

| Bug | Description | Solution |
|-----|-------------|----------|
| Budget total always 0 when using decimal commas | On the budget page, the “Total” value stayed at 0 even when rows had valid quantities and unit costs like `1,50` and `2,75`. The problem was that `parseFloat("1,50")` returns `NaN`, so all rows contributed `0` to the total. | The JS total calculation was updated to normalise decimal commas before parsing (`value.replace(',', '.')`) and, in one iteration, to use `input.valueAsNumber` where supported. During debugging, the inputs were also given explicit CSS classes (`js-qty`, `js-unit`) in `BudgetItemForm` so the script could reliably select the correct fields inside each `<tr>`, independent of Django formset field names. After these changes, the total updated correctly for both dot and comma decimal formats. |
| Budget JS selectors not matching rendered inputs | Early versions of the script tried to select inputs using `name$="-quantity"` and `name$="-unit_cost"`. This was brittle: if the management form or formset prefix changed, or if the selector ran on unrelated tables, nothing was found and the total stayed at 0. | During testing, the rendered HTML was inspected in DevTools and it became clear that targeting by name was fragile. `BudgetItemForm` widgets were updated to include `class="js-qty"` and `class="js-unit"`. The total calculation now loops through each table row and queries these classes, making the selectors stable and much easier to reason about while debugging. |
| Story score not displaying correctly (`aggregate_total`) | In `story_detail.html`, the story score was rendered using `{{ object.votes.aggregate_total }}`, but that attribute does not exist. This led to either empty output or confusing values. | The fix was to move the score aggregation to the view. `StoryDetail.get_context_data` now computes `ctx["score"] = self.object.votes.aggregate(total=Sum("value"))["total"] or 0`. The template displays `{{ score }}` instead of a non-existent attribute. This separation made the score easier to test and ensured the value always matches the DB aggregate. |
| Story comment scores missing | Story comments were rendered but had no visible scores, even though a `CommentVote` model existed. There was no annotation on the comments queryset, so the template had no `c.score` to show. | The comments queryset in `StoryDetail` was updated to: `Comment.objects.filter(...).annotate(score=Sum("votes__value"))`. In `story_detail.html`, a small line was added below each comment body: `Comment score: {{ c.score|default:"0" }}`. After reloading, voting on comments and refreshing the page showed the expected scores. |
| Review comment scores behaving unexpectedly (e.g. 0 → 2 → 0) | During local testing, review comment scores sometimes jumped by 2 when a user upvoted, for example 0 → 2 → 0 on repeated clicks. This behaviour came from how the existing votes were stored: if multiple rows existed in `ReviewCommentVote` for the same user and comment (before `unique_together` was enforced), or if multiple users had already voted, the sum appeared to “jump” more than expected. | First, the DB state for `ReviewCommentVote` was inspected to confirm duplicates and multi-user scenarios. Once understood, the behaviour was refined to a clearer model where each user’s contribution is always in { -1, 0, +1 }.|
| Review comment voting toggle logic unintuitive | The initial toggle logic simply deleted a vote if the same value was clicked again. The product requirement evolved to: each user should add +1 to the global score on their first upvote (on top of other users’ votes), and subtract 1 when downvoting. Users should have at most one vote per comment, and their “contribution” should cycle cleanly between -1, 0 and +1. | `ReviewCommentVoteToggle` was refactored to treat each user’s vote as a small state machine. On POST, the view loads or creates the `ReviewCommentVote` with a default of 0. If the submitted value is `1`, it sets `new = min(current + 1, 1)`; if `-1`, it sets `new = max(current - 1, -1)`. When `new == 0`, the row is deleted (meaning “no vote”). This guarantees that each click changes the global score by exactly ±1 from that user, and that a user can only ever contribute -1, 0 or +1 to each comment. Testing this by clicking `+` then `-` and vice versa confirmed that scores changed in predictable, single-step increments. |
| Confusion after hiding story upvote/downvote buttons | As part of design tweaks, the story upvote/downvote buttons and their supporting `<script>` were temporarily removed from `story_detail.html`, but the expectation remained that the score should “move” in real time. Without any buttons or JS left to send votes, the score naturally remained static. | The testing process made it clear that real-time score changes depend on both a POST endpoint (`VoteToggle`) and client-side JS. For pages where live interaction is desired, the buttons and their `fetch` logic were restored, and `#score` is updated from the JSON response. For pages where votes should be “read-only” (for example, when viewing as a guest or in a simpler UI), the score is purely rendered from the backend context, and any missing live update is now treated as expected behaviour rather than a bug. |

#### Detailed Debug Notes

Below is a more narrative summary of the main debugging sessions that influenced the final implementation.

##### Budget Total Debugging

1. **Symptom:**  
   - On the budget edit/create page, the “Total” display stayed at `0.00` regardless of input.
   - Changing quantities and unit costs appeared to have no effect.

2. **Initial Findings:**  
   - Logging to the console showed that `parseFloat` returned `NaN` for values like `"12,50"`.
   - In a Swedish locale, users naturally entered values with commas as decimal separators.
   - The JS was also querying `input[name$="unit_cost"]` and `input[name$="quantity"]`, which did not match reliably when formset prefixes varied.

3. **Fix Steps:**  
   - Updated `BudgetItemForm` to give `quantity` and `unit_cost` consistent CSS classes (`js-qty` and `js-unit`).
   - Simplified the JS to:
     - Iterate over each `<tr>` in the table.
     - Select `.js-qty` and `.js-unit` within that row.
     - Normalise the value using `String(value).replace(',', '.')` before calling `parseFloat`.
   - In one iteration, `input.valueAsNumber` was tested to let the browser handle locale conversion automatically.
   - After these changes, manual tests with combinations like `1,5 × 100`, `0,25 × 3`, and `2 × 50` correctly updated the total.

4. **Result:**  
   - Total now updates correctly for both comma and dot decimals.
   - The code is resilient to template changes because it relies on explicit classes instead of name suffix guessing.

##### Review Comment Voting Debugging

1. **Symptom (original):**  
   - Comment scores sometimes appeared to jump unexpectedly (e.g. 0 → 2 → 0) when repeatedly clicking the upvote button in local testing.
   - It was unclear if this was a bug in the logic, test data, or expectations.

2. **Investigation:**  
   - The `ReviewCommentVote` model was designed to have `unique_together = ("comment", "user")`, but old data or manual inserts could create duplicates.
   - The score is calculated as `Sum("votes__value")`, so:
     - Multiple users voting would legitimately produce values greater than 1.
     - Duplicate rows for one user could also inflate the score.
   - Using the Django shell and admin, votes for specific comments were inspected to understand which rows were involved.

3. **Clarifying Desired Behaviour:**  
   - Each user should contribute at most one of three states to each comment: -1, 0, +1.
   - Clicking up for the first time adds +1 on top of any existing votes from other users.
   - Clicking down after up should reduce the overall score by 1 (moving the user’s contribution from +1 to 0, or 0 to -1).
   - Repeated clicks in the same direction should not cause score changes beyond the -1/+1 bounds.

4. **Fix Steps:**  
   - Implemented the tri-state logic in `ReviewCommentVoteToggle`:
     - Load or create `ReviewCommentVote` with `defaults={"value": 0}`.
     - Track the current value (`current`).
     - If form sends `value == 1`, set `new = min(current + 1, 1)`.
     - If form sends `value == -1`, set `new = max(current - 1, -1)`.
     - If `new == 0`, delete the vote row to represent “no vote”.
   - Re-tested by:
     - Clicking `+` repeatedly (observing 0 → 1 → 1).
     - Clicking `-` repeatedly (0 → -1 → -1).
     - Clicking `+` then `-` (0 → 1 → 0).
     - Clicking `-` then `+` (0 → -1 → 0).

5. **Result:**  
   - Scores now change by exactly ±1 per click for each user.
   - The relationship between user actions and total scores is predictable and easy to explain.

##### Story Score and Comment Score Debugging

1. **Symptom:**  
   - The story’s score display was bound to `{{ object.votes.aggregate_total }}`, which never reflected the actual aggregate.
   - Story comments did not show any scores despite having a `CommentVote` model.

2. **Fix Steps (Story Score):**  
   - Moved aggregation into `StoryDetail.get_context_data`:
     - `ctx["score"] = self.object.votes.aggregate(total=Sum("value"))["total"] or 0`.
   - Updated the template to use `{{ score }}` instead of a non-existent `aggregate_total` property.
   - Tested by creating/updating `Vote` rows and confirming the displayed score matched the DB.

3. **Fix Steps (Story Comment Scores):**  
   - Updated the comments queryset in `StoryDetail` to:
     - `Comment.objects.filter(story=self.object, parent__isnull=True).annotate(score=Sum("votes__value"))`.
   - Added `Comment score: {{ c.score|default:"0" }}` under each comment in `story_detail.html`.
   - Verified that after voting on comments and reloading, the displayed scores matched the aggregated `CommentVote.value` sums.

4. **Result:**  
   - Both story scores and story comment scores now reflect database values correctly.
   - The separation of concerns (aggregation in the view, simple display in the template) improved testability.

---

### Known Bugs

| Bug | Description |
|-----|-------------|
| Comment scores only update on full page reload | For both reviews and stories, comment scores are recalculated on the server and rendered on page load. After a comment vote, the user is redirected, which refreshes the scores. There is currently no inline AJAX update for individual comment scores. |
| Budget total depends on JavaScript | Users with JavaScript disabled will not see the live-updating total on the budget page. Form submission still works and server-side data is correct, but the convenience total is JS-only. |
| Story comment voting and review comment voting logic not yet unified | Review comments use the refined tri-state logic (-1, 0, +1). Story comment voting is functionally correct but does not yet share a common helper, leading to duplicated logic that could be refactored into a shared utility. |

---
