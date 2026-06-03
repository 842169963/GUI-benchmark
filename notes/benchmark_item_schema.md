# Benchmark Item Schema

Status: planning specification for fixed benchmark items.

A benchmark item is the fixed test specification used to evaluate generator
models. It is not a generated output.

A generated artifact is the web app produced by a generator model for one
benchmark item. The artifact is the direct evaluation target.

A model-level leaderboard row aggregates artifact-level scores across benchmark
items for one generator LLM or model configuration.

## Directory Shape

Recommended benchmark item shape:

```text
benchmark_item/
  requirement.md
  pages.json
  elements.json
  tasks.json
  validation_rules.json
  visual_pages.json
  metadata.json
```

The repository may keep Vision2Web-derived files in the existing
`data/track_b/items/` layout, but the benchmark semantics should map to the
schema above.

## File Meanings

### `requirement.md`

Natural-language requirement given to the generator model.

It should describe the intended web interface, target domain, required pages,
important content, and expected interactions. It should not include hidden
evaluation answers that are not part of the user-facing specification.

### `pages.json`

Expected pages or routes for the generated app.

Example:

```json
{
  "pages": [
    {"id": "home", "path": "/", "label": "Home"},
    {"id": "products", "path": "/products", "label": "Products"},
    {"id": "cart", "path": "/cart", "label": "Cart"},
    {"id": "checkout", "path": "/checkout", "label": "Checkout"}
  ]
}
```

### `elements.json`

Required elements per page, including headings, text, buttons, links, forms,
tables, cards, labels, and required selectors when applicable.

Example:

```json
{
  "elements": [
    {
      "page_id": "products",
      "type": "button",
      "label": "Add to Cart",
      "required": true
    },
    {
      "page_id": "checkout",
      "type": "input",
      "label": "Email",
      "required": true
    }
  ]
}
```

### `tasks.json`

Dynamic user tasks that can be validated by the benchmark.

Example:

```json
{
  "tasks": [
    {
      "id": "add_product_to_cart",
      "instruction": "Add one product to the cart.",
      "start_page": "products",
      "success_rule": "cart_count_increases"
    },
    {
      "id": "submit_checkout_form",
      "instruction": "Complete the checkout form and submit it.",
      "start_page": "checkout",
      "success_rule": "confirmation_visible"
    }
  ]
}
```

### `validation_rules.json`

Rules used to judge static and dynamic requirements.

Example:

```json
{
  "rules": [
    {
      "id": "products_has_add_button",
      "category": "static_technical",
      "page_id": "products",
      "check": "element_text_present",
      "value": "Add to Cart"
    },
    {
      "id": "cart_updates_after_add",
      "category": "dynamic",
      "task_id": "add_product_to_cart",
      "check": "state_change",
      "value": "cart_count_increases"
    }
  ]
}
```

Static rules check structure and coverage. Dynamic rules check behavior after
interaction or validated workflow execution.

### `visual_pages.json`

Predefined pages or routes that must be screenshotted for static visual
evaluation.

Example:

```json
{
  "viewport": {"width": 1440, "height": 900},
  "pages": [
    {"page_id": "home", "path": "/"},
    {"page_id": "products", "path": "/products"},
    {"page_id": "checkout", "path": "/checkout"}
  ]
}
```

Static visual scoring must use these standardized predefined-route screenshots.
Agent trace screenshots are only for debugging and dynamic failure analysis.

### `metadata.json`

Item metadata used for filtering, reporting, and reproducibility.

Example:

```json
{
  "item_id": "shop_checkout_001",
  "source": "Vision2Web-derived",
  "category": "e-commerce",
  "difficulty": "medium",
  "requires_dynamic_validation": true,
  "has_local_assets": true,
  "notes": "Prototype includes products, cart, and checkout workflow."
}
```

## Generated Artifact Metadata

Every generated artifact should store generation metadata separately from the
benchmark item:

```json
{
  "item_id": "shop_checkout_001",
  "model": "example-generator-model",
  "provider": "example-provider",
  "prompt_id": "TB-GEN-vX",
  "timestamp": "2026-06-03T12:00:00+02:00",
  "input_tokens": 12345,
  "output_tokens": 6789,
  "total_tokens": 19134,
  "estimated_cost_usd": 0.42,
  "latency_seconds": 85.2,
  "finish_reason": "stop"
}
```

The benchmark item remains fixed. The generated artifact and its metadata vary
by generator model and run.

## Result Levels

Artifact-level result:

```text
one generated artifact for one benchmark item from one generator model
```

Model-level result:

```text
aggregate of artifact-level results across the fixed benchmark item set
```

The thesis should always make this distinction explicit.
