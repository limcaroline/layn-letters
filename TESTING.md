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
    - [Sample Solved Bugs](#solved-bugs)



---

## Responsiveness

Layn Letters was tested across a range of viewport sizes using Chrome DevTools device toolbar to ensure a consistent experience on mobile, tablet and desktop.

### Mobile Screenshots

- Home

  ![Home – Mobile](resources/testing/mobile-1.png)

- Reviews

  ![Reviews – Mobile](resources/testing/mobile-2.png)

- Stories

  ![Stories – Mobile](resources/testing/mobile-3.png)

- Budgets

  ![Budgets – Mobile](resources/testing/mobile-4.png)

### Tablet Screenshots

- Home

  ![Home – Tablet](resources/testing/tablet-1.png)

- Reviews

  ![Reviews – Tablet](resources/testing/tablet-2.png)

- Stories

  ![Stories – Tablet](resources/testing/tablet-3.png)

- Budgets

  ![Budgets – Tablet](resources/testing/tablet-4.png)

### Desktop Screenshots

- Home

  ![Home – Desktop](resources/testing/desktop-1.png)

- Reviews

  ![Reviews – Desktop](resources/testing/desktop-2.png)

- Stories

  ![Stories – Desktop](resources/testing/desktop-3.png)

- Budgets

  ![Budgets – Desktop](resources/testing/desktop-4.png)

---

## Validations

### W3C Validator

All top-level rendered templates were checked using:

- W3C HTML Validator: https://validator.w3.org/
- W3C CSS Validator: https://jigsaw.w3.org/css-validator/


- HTML check returned no errors.

  ![HTML validation – before fixes](resources/testing/html-check.png)


- CSS check returned no errors.

  ![CSS validation – no errors](resources/testing/css-check.png)

### JSHint

JavaScript was validated with https://jshint.com/.

  ![JSHint fixed](resources/testing/jshint-check.png)

### Python Linter

Python code was validated using the Code Institute Python Linter (flake8-equivalent) across apps such as `reviews`, `stories`, `budgets` and `core`.

Example:

- No errors reported after minor formatting adjustments (line length, spacing, imports).

  ![Python linter – no errors](resources/testing/python-check-stories-views.png)
  ![Python linter – no errors](resources/testing/python-check-stories-models.png)

---

## Lighthouse

Lighthouse audits (Performance, Accessibility, Best Practices, SEO) were run from Chrome DevTools on key pages:

- Home
- Reviews list and detail
- Story list and detail
- Budget list and budget edit

Example report:

![Lighthouse testing results](resources/testing/lighthouse.png)

Where possible, minor issues such as missing `alt` attributes and low-contrast text were corrected to improve scores.

---

## Wave Webaim

Accessibility was checked using the WAVE browser extension: https://wave.webaim.org/

Results, among others:

- No critical accessibility errors on content pages.
- Color contrast checks passed after minor design adjustments.

![WAVE results](resources/testing/wave-before.png)
![WAVE results](resources/testing/wave-after.png)

---

## Browser Compatibility

Tested on latest stable versions:

- Chrome
- Safari


- Safari screenshot:
  ![Safari 1](resources/testing/browsers/safari.png)  

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

### Budgets

**Budget Form and Items**

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
|--------|------------------|-------------------|--------|-----------|
| Create budget | Saves budget title, currency and notes. | Submitted valid form. | Budget created and visible in list. | Pass |
| Formset items | Each item includes day, name, category, quantity, unit cost, notes. | Added multiple items. | All fields saved. | Pass |
| Delete existing item | Delete checkbox removes item on save. | Ticked Delete on one row. | Item removed after submit. | Pass |


### Authentication

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
|--------|------------------|-------------------|--------|-----------|
| Signup | New user can register an account. | Submitted signup form. | User created and logged in. | Pass |
| Login | Existing user can log in. | Logged in with valid credentials. | Login succeeded. | Pass |
| Logout | User is logged out and redirected. | Clicked Logout link. | Session cleared. | Pass |
| Auth-only views | Protected views require login. | Visited protected URLs logged out. | Redirected to login. | Pass |
| Owner-only review/story actions | Only site owner or author can edit/delete. | Attempted edit/delete as different users. | Access restricted correctly. | Pass |

---

## Bugs and Debugging

#### Example

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