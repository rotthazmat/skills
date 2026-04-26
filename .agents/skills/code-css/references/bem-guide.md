# BEM Naming Guide

Convention: `ComponentName-element`, `ComponentName--modifier`

## Component (block)

The root class uses PascalCase:

```css
.UserCard { ... }
.NavMenu { ... }
.ProductList { ... }
```

## Element

A part inside a component uses a single hyphen:

```css
.UserCard-avatar { ... }
.UserCard-name { ... }
.UserCard-actions { ... }
.NavMenu-item { ... }
.NavMenu-link { ... }
```

## Modifier

A variation uses double hyphens:

```css
.UserCard--featured { ... }
.UserCard--compact { ... }
.NavMenu--horizontal { ... }
.NavMenu-item--active { ... }   /* modifier on an element */
```

---

## Gotchas

### Use BEM classes, not descendant selectors

```css
/* WRONG — fragile descendant selector */
.UserCard .avatar { ... }
.UserCard img { ... }

/* CORRECT — flat BEM element */
.UserCard-avatar { ... }
```

### Alphabetical properties inside every block

```scss
/* CORRECT */
.UserCard {
  background: #fff;
  border-radius: 4px;
  color: #333;
  display: flex;
  padding: 16px;
}

/* WRONG — unsorted */
.UserCard {
  display: flex;
  background: #fff;
  padding: 16px;
  color: #333;
  border-radius: 4px;
}
```

### Max 1 ID selector per rule

```css
/* WRONG — two IDs in one rule */
#sidebar #logo { ... }

/* CORRECT — split or use a class */
#sidebar { ... }
.Sidebar-logo { ... }
```

### No duplicate properties in a block

```scss
/* WRONG */
.NavMenu {
  background: white;
  background: #f5f5f5;  /* duplicate — only one survives */
}

/* CORRECT */
.NavMenu {
  background: #f5f5f5;
}
```

### No duplicate `$` variables across a file

```scss
/* WRONG */
$primary: #333;
$spacing: 16px;
$primary: #444;   /* duplicate — causes silent override */

/* CORRECT */
$primary: #444;
$spacing: 16px;
```
